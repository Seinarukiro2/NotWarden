import logging
from telethon import TelegramClient, events, Button
from dotenv import load_dotenv
import os
from db.crud import crud_topic, crud_message
from db.base import SessionLocal
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

@client.on(events.NewMessage(pattern='/start'))
async def start_command_handler(event):
    async with SessionLocal() as db:
        async with db.begin():
            # Получение всех топиков из базы данных
            topics = await crud_topic.get_all_topics(db)

            # Загрузка всех атрибутов, которые могут понадобиться
            topics = [topic.name for topic in topics]

    # Создание кнопок на основе топиков
    buttons = [
        [Button.inline(topic)] for topic in topics
    ]

    # Отправка сообщения с клавиатурой кнопок
    await event.respond(
        "Выберите интересующий вас топик:",
        buttons=buttons
    )

    logger.info(f"Отправлены кнопки с топиками для пользователя {event.sender_id}")

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')

    if data == 'back_to_topics':
        await event.delete()
        await start_command_handler(event)
        return

    async with SessionLocal() as db:
        async with db.begin():
            topic = await crud_topic.get_topic(db, data)

            if not topic:
                await event.edit("Топик не найден.")
                await asyncio.sleep(3)
                await event.delete()
                await start_command_handler(event)
                return

            messages = await crud_message.get_messages_by_topic(db, topic)
            if not messages:
                await event.edit("Сообщений для этого топика пока нет.")
                await asyncio.sleep(3)
                await event.delete()
                await start_command_handler(event)
                return

            messages_text = "\n".join([msg.message_link for msg in messages])

    # Редактируем сообщение, чтобы показать ссылки на сообщения в топике
    await event.edit(
        f"📜 **Сообщения в топике** '{data}':\n\n{messages_text}",
        buttons=[Button.inline("🔙 Назад", data='back_to_topics')]
    )

@client.on(events.NewMessage)
@error_wrapper(logger)
async def new_message_listener(event):
    """
    Основной обработчик для новых сообщений. Вызывает функции для обработки сообщения
    и создания новых топиков, если это требуется.
    
    :param event: Событие нового сообщения.
    """
    if event.message.message.startswith('/start'):
        return  # Пропускаем обработку команды /start

    await handle_new_message(event, logger)
    await new_topic_message(event, logger)


@client.on(events.NewMessage)
@error_wrapper(logger)
async def new_message_listener(event):
    """
    Основной обработчик для новых сообщений. Вызывает функции для обработки сообщения
    и создания новых топиков, если это требуется.
    
    :param event: Событие нового сообщения.
    """
    if event.message.message.startswith('/start'):
        return  # Пропускаем обработку команды /start

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
