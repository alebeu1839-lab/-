import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def generate_caption(topic: str, tone: str = "親しみやすい") -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Instagram投稿用のキャプションを作成してください。\n"
                    f"テーマ: {topic}\n"
                    f"トーン: {tone}\n"
                    f"絵文字を適度に使い、最後に関連ハッシュタグを5個程度つけてください。"
                ),
            }
        ],
    )
    return message.content[0].text
