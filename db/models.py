from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .base import Base


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    messages = relationship("Message", back_populates="topic")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    message_link = Column(String, nullable=False)

    topic = relationship("Topic", back_populates="messages")
