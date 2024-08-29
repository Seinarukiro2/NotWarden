import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
from methods.message_handler import handle_new_message
from methods.new_topic_message import new_topic_message
from decorators.error_wrapper import error_wrapper
from db.base import init_db

# Load environment variables from .env file
load_dotenv()

# Get data from .env
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create a client instance
client = TelegramClient("bot_session", api_id, api_hash)


@client.on(events.NewMessage)
@error_wrapper(logger)
async def new_message_listener(event):
    """
    Основной обработчик для новых сообщений. Вызывает функции для обработки сообщения
    и создания новых топиков, если это требуется.
    
    :param event: Событие нового сообщения.
    """

    await handle_new_message(event, logger)
    await new_topic_message(event, logger)



# Start the bot
async def main():
    await init_db()
    await client.start(bot_token=bot_token)
    logger.info("Bot started...")
    await client.run_until_disconnected()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
