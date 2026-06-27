import os

import requests

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


def get_media_insights(media_id: str) -> dict:
    access_token = os.environ["IG_ACCESS_TOKEN"]
    metrics = "impressions,reach,engagement,saved"
    response = requests.get(
        f"{GRAPH_API_BASE}/{media_id}/insights",
        params={"metric": metrics, "access_token": access_token},
    ).json()
    return {item["name"]: item["values"][0]["value"] for item in response.get("data", [])}


def get_account_summary() -> dict:
    access_token = os.environ["IG_ACCESS_TOKEN"]
    ig_user_id = os.environ["IG_BUSINESS_ACCOUNT_ID"]
    response = requests.get(
        f"{GRAPH_API_BASE}/{ig_user_id}",
        params={
            "fields": "followers_count,media_count",
            "access_token": access_token,
        },
    ).json()
    return response
