import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from sns_automation.analytics import get_media_insights
from sns_automation.content_generator import generate_caption
from sns_automation.poster import post_image

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# (画像URL, テーマ) のキューを投稿予定として並べておく
POST_QUEUE = [
    ("https://example.com/photo1.jpg", "今日のおすすめスポット"),
]

posted_media_ids: list[str] = []


def run_scheduled_post() -> None:
    if not POST_QUEUE:
        logger.info("投稿キューが空です")
        return
    image_url, topic = POST_QUEUE.pop(0)
    caption = generate_caption(topic)
    media_id = post_image(image_url, caption)
    posted_media_ids.append(media_id)
    logger.info("投稿完了: %s", media_id)


def run_analytics_report() -> None:
    for media_id in posted_media_ids:
        insights = get_media_insights(media_id)
        logger.info("media_id=%s insights=%s", media_id, insights)


def main() -> None:
    scheduler = BlockingScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(run_scheduled_post, "cron", hour=9)
    scheduler.add_job(run_analytics_report, "cron", hour=21)
    logger.info("スケジューラ起動: 毎日9時に投稿、21時に分析レポート")
    scheduler.start()


if __name__ == "__main__":
    main()
