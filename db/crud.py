from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Topic, Message


class CRUDTopic:
    async def get_topic(self, db: AsyncSession, name: str) -> Topic:
        result = await db.execute(select(Topic).filter(Topic.name == name))
        return result.scalars().first()

    async def create_topic(self, db: AsyncSession, name: str) -> Topic:
        db_topic = Topic(name=name)
        db.add(db_topic)
        await db.commit()
        await db.refresh(db_topic)
        return db_topic

    async def get_or_create_topic(self, db: AsyncSession, name: str) -> Topic:
        topic = await self.get_topic(db, name)
        if not topic:
            topic = await self.create_topic(db, name)
        return topic
    
    async def get_all_topics(self, db: AsyncSession):
        result = await db.execute(select(Topic))
        return result.scalars().all()

class CRUDMessage:
    async def create_message(
        self, db: AsyncSession, topic: Topic, message_link: str
    ) -> Message:
        db_message = Message(topic_id=topic.id, message_link=message_link)
        db.add(db_message)
        await db.commit()
        await db.refresh(db_message)
        return db_message

    async def get_messages_by_topic(self, db: AsyncSession, topic: Topic):
        result = await db.execute(select(Message).filter(Message.topic_id == topic.id))
        return result.scalars().all()



crud_topic = CRUDTopic()
crud_message = CRUDMessage()
