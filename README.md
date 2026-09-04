# linux-telegram-bot

A Python Telegram bot that posts the latest tech/Linux headlines on a schedule. It reads headlines from a configurable source (defaults to Hacker News) and optionally triggers a GitHub webhook listener that notifies a chat on every push.

## Features

- **`bot.py`** — posts the top headlines every hour, plus `/start` and `/news` commands for manual triggers.
- **`webhook_listener.py`** — tiny Flask endpoint that receives a GitHub webhook and posts commit notifications to Telegram.

## Setup

### 1. Create a bot

1. Message [@BotFather](https://t.me/BotFather) → `/newbot` → copy the bot token.
2. Get your **numeric** chat id (message your bot, then call `https://api.telegram.org/bot<TOKEN>/getUpdates` and read `message.chat.id`).

### 2. Configure

```bash
cp .env.example .env
# fill in TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
```

On Windows PowerShell you can also export inline:

```powershell
$env:TELEGRAM_TOKEN="..."
$env:TELEGRAM_CHAT_ID="..."
```

### 3. Install & run

```bash
pip install -r requirements.txt
python bot.py
```

The bot will post the latest headlines immediately, then every hour. Use `/news` in chat for an on-demand update.

## GitHub webhook (optional)

Run the listener:

```bash
python webhook_listener.py
```

Then in your GitHub repo → **Settings → Webhooks → Add webhook**:

- **Payload URL**: `http://<your-host>:5000/webhook`
- **Content type**: `application/json`

Every push posts a commit summary to your chat. (For local testing, use a tunnel like `ngrok`.)

## Configuration

| Variable          | Default                     | Purpose                              |
| ----------------- | --------------------------- | ------------------------------------ |
| `TELEGRAM_TOKEN`  | _(required)_                | Bot token from BotFather             |
| `TELEGRAM_CHAT_ID`| _(required)_                | Numeric chat/channel id              |
| `NEWS_URL`        | `https://news.ycombinator.com/` | News source to scrape            |
| `HEADLINES`       | `5`                         | How many headlines to post           |
| `PORT`            | `5000`                      | Webhook listener port                |

## Security notes

- The Telegram token and chat id are read from environment variables — never hardcode them.
- **If a token was ever committed publicly, rotate it immediately in BotFather.**

## License

MIT
