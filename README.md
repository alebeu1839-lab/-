# Instagram SNS運用自動化

キャプション生成、自動投稿、分析レポートを自動化する最小構成。

## セットアップ

```bash
pip install -r requirements.txt
cp .env.example .env
# .env に ANTHROPIC_API_KEY / IG_ACCESS_TOKEN / IG_BUSINESS_ACCOUNT_ID を設定
```

`IG_ACCESS_TOKEN` / `IG_BUSINESS_ACCOUNT_ID` は Instagram ビジネス/クリエイターアカウントを
Facebookページに連携した上で、Meta for Developers でアプリを作成し取得する。

## 構成

- `sns_automation/content_generator.py`: Claude APIでキャプション生成
- `sns_automation/poster.py`: Instagram Graph APIで画像投稿
- `sns_automation/analytics.py`: 投稿のインサイト・アカウント情報取得
- `sns_automation/scheduler.py`: 毎日定時に投稿・分析を自動実行

## 実行

```bash
python -m sns_automation.scheduler
```

`POST_QUEUE`（scheduler.py内）に画像URLとテーマを追加してキューに積む運用。
