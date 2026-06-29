import logging

import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from sns_automation.analytics import get_media_insights
from sns_automation.content_generator import generate_caption
from sns_automation.poster import post_image

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

POST_QUEUE = list(config["posts"])
posted_media_ids: list[str] = []


def run_scheduled_post() -> None:
    if not POST_QUEUE:
        logger.info("投稿キューが空です")
        return
    post = POST_QUEUE.pop(0)
    caption = generate_caption(
        post["topic"],
        tone=config["account"]["tone"],
        hashtags_count=config["account"]["hashtags_count"],
    )
    media_id = post_image(post["image_url"], caption)
    posted_media_ids.append(media_id)
    logger.info("投稿完了: %s", media_id)


def run_analytics_report() -> None:
    for media_id in posted_media_ids:
        insights = get_media_insights(media_id)
        logger.info("media_id=%s insights=%s", media_id, insights)


def main() -> None:
    scheduler = BlockingScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(run_scheduled_post, "cron", hour=config["schedule"]["post_hour"])
    scheduler.add_job(run_analytics_report, "cron", hour=config["schedule"]["report_hour"])
    logger.info(
        "スケジューラ起動: 毎日%d時に投稿、%d時に分析レポート",
        config["schedule"]["post_hour"],
        config["schedule"]["report_hour"],
    )
    scheduler.start()


if __name__ == "__main__":
    main()
