from telethon import events


async def handle_new_message(event: events.NewMessage.Event, logger):
    """
    Обрабатывает новые сообщения и удаляет те, которые содержат ?startapp.

    :param event: Событие нового сообщения.
    :param logger: Логгер для логирования событий.
    """
    message_text = event.message.message
    chat_id = event.chat_id
    sender_id = event.sender_id

    # Логируем полученное сообщение
    logger.info(
        f"Получено сообщение от пользователя {sender_id} в чате {chat_id}: {message_text}"
    )

    # Проверяем, содержит ли сообщение строку "?startapp"
    if "?startapp" in message_text:
        await event.delete()
        logger.info(f"Сообщение от пользователя {sender_id} в чате {chat_id} удалено.")
