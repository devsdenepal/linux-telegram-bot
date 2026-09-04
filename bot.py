import asyncio
import logging
import os

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")  # numeric chat/channel/group id
NEWS_URL = os.environ.get("NEWS_URL", "https://news.ycombinator.com/")
HEADLINES = int(os.environ.get("HEADLINES", "5"))


def fetch_linux_news(url=NEWS_URL, count=HEADLINES):
    """Fetch the top headlines from a tech news site."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    # Hacker News titles live in .titleline a elements
    items = soup.select("span.titleline a")
    return [a.get_text(strip=True) for a in items[:count]]


async def send_linux_news(application: Application):
    """Fetch headlines and post them to the configured chat."""
    try:
        headlines = fetch_linux_news()
    except Exception as e:
        logger.error("Failed to fetch news: %s", e)
        return
    message = "\n".join(f"{i + 1}. {h}" for i, h in enumerate(headlines))
    await application.bot.send_message(chat_id=CHAT_ID, text=f"Latest tech headlines:\n\n{message}")
    logger.info("News sent successfully.")


async def periodic_news_updates(application: Application):
    while True:
        try:
            await send_linux_news(application)
        except Exception as e:
            logger.error("Error sending news: %s", e)
        await asyncio.sleep(3600)  # Wait 1 hour before the next update


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This bot posts the latest tech headlines every hour. "
        "Use /news to trigger an immediate update."
    )


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        headlines = fetch_linux_news()
    except Exception as e:
        await update.message.reply_text(f"Couldn't fetch news: {e}")
        return
    message = "\n".join(f"{i + 1}. {h}" for i, h in enumerate(headlines))
    await update.message.reply_text(f"Latest tech headlines:\n\n{message}")


async def main():
    if not TOKEN:
        raise SystemExit("TELEGRAM_TOKEN is not set.")
    if not CHAT_ID:
        raise SystemExit("TELEGRAM_CHAT_ID is not set.")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", news))

    # Send an update once immediately, then every hour
    application.create_task(periodic_news_updates(application))

    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
