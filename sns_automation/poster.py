import os
import time

import requests

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


def post_image(image_url: str, caption: str) -> str:
    access_token = os.environ["IG_ACCESS_TOKEN"]
    ig_user_id = os.environ["IG_BUSINESS_ACCOUNT_ID"]

    container = requests.post(
        f"{GRAPH_API_BASE}/{ig_user_id}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token,
        },
    ).json()
    if "id" not in container:
        raise RuntimeError(f"Failed to create media container: {container}")
    creation_id = container["id"]

    for _ in range(10):
        status = requests.get(
            f"{GRAPH_API_BASE}/{creation_id}",
            params={"fields": "status_code", "access_token": access_token},
        ).json()
        if status.get("status_code") == "FINISHED":
            break
        time.sleep(2)

    publish = requests.post(
        f"{GRAPH_API_BASE}/{ig_user_id}/media_publish",
        data={"creation_id": creation_id, "access_token": access_token},
    ).json()
    if "id" not in publish:
        raise RuntimeError(f"Failed to publish media: {publish}")
    return publish["id"]
