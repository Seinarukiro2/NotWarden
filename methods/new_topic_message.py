from db.crud import crud_topic, crud_message
from db.base import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def new_topic_message(event, logger):
    try:
        message_text = event.message.message
        message_link = f"https://t.me/c/{event.chat_id}/{event.message.id}"

        if "support" in message_text:
            topic_name = "support"
        elif "bug" in message_text:
            topic_name = "bug"
        elif "question" in message_text:
            topic_name = "question"
        elif "idea" in message_text:
            topic_name = "idea"
        else:
            logger.info(f"Не удалось определить топик для сообщения: {message_text}")
            return

        async with SessionLocal() as db:
            async with db.begin():  # Начало транзакции
                # Получение или создание топика
                topic = await crud_topic.get_or_create_topic(db, topic_name)
                logger.info(f"Топик найден или создан: {topic.name}")
                
                # Сохранение сообщения
                await crud_message.create_message(db, topic, message_link)
                logger.info("Сообщение сохранено")


    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")