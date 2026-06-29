# Instagram SNS運用自動化

キャプション生成、自動投稿、分析レポートを自動化する最小構成。

運用する人は **`config.yaml` を編集するだけ**でよく、コードを触る必要はない。

## セットアップ（最初の1回だけ）

```bash
pip install -r requirements.txt
cp .env.example .env
# .env に ANTHROPIC_API_KEY / IG_ACCESS_TOKEN / IG_BUSINESS_ACCOUNT_ID を設定
```

`IG_ACCESS_TOKEN` / `IG_BUSINESS_ACCOUNT_ID` は Instagram ビジネス/クリエイターアカウントを
Facebookページに連携した上で、Meta for Developers でアプリを作成し取得する。

## 運用（毎回これだけ）

`config.yaml` を編集して方向性を決める。

```yaml
account:
  tone: "親しみやすい"   # 投稿の口調
  hashtags_count: 5

schedule:
  post_hour: 9           # 投稿する時刻
  report_hour: 21        # 分析レポートを出す時刻

posts:                   # 投稿予定。上から順に消費される
  - image_url: "https://example.com/photo1.jpg"
    topic: "今日のおすすめスポット"
```

保存したら起動する。

```bash
python -m sns_automation.scheduler
```

毎日`post_hour`に`posts`の先頭からキャプションをAIが自動生成して投稿し、
`report_hour`に過去投稿の分析結果をログ出力する。

## 構成（コードを変更する場合のみ参照）

- `config.yaml`: 運用の方向性（テーマ・トーン・投稿時刻・投稿キュー）
- `sns_automation/content_generator.py`: Claude APIでキャプション生成
- `sns_automation/poster.py`: Instagram Graph APIで画像投稿
- `sns_automation/analytics.py`: 投稿のインサイト・アカウント情報取得
- `sns_automation/scheduler.py`: config.yamlを読み込み、定時に投稿・分析を自動実行
