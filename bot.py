import logging
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to fetch Linux/Tech news
async def fetch_linux_news():
    url = 'https://news.ycombinator.com/'  # Replace with desired Linux/tech news site
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract headlines from the news site (modify as per site structure)
    headlines = [item.get_text() for item in soup.find_all('a', class_='storylink')[:5]]  # Fetch top 5 headlines
    return headlines

# Function to send news to a specific Telegram chat
async def send_linux_news(application):
    chat_id = "krimsonsquad"  # Replace with the ID of the chat/group/channel you want to send news to
    news = await fetch_linux_news()
    news_message = "\n".join(f"{idx+1}. {headline}" for idx, headline in enumerate(news))
    
    # Send the message
    await application.bot.send_message(chat_id=chat_id, text=f"Here are the latest tech headlines:\n\n{news_message}")

# Function to run the periodic task in the background
async def periodic_news_updates(application):
    while True:
        try:
            await send_linux_news(application)
            logger.info("News sent successfully.")
        except Exception as e:
            logger.error(f"Error sending news: {e}")
        
        await asyncio.sleep(3600)  # Wait for 1 hour before sending the next update

# Main function
async def main():
    application = Application.builder().token("").build()

    # Start the background task for sending news automatically
    application.job_queue.run_once(periodic_news_updates(application), 0)

    # Start polling for any manual commands (if needed)
    await application.start_polling()
    await application.idle()

if __name__ == '__main__':
    asyncio.run(main())
