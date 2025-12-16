from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs01"

    id = Column(Integer, primary_key=True)
    role = Column(String(10))       # "user" | "ai"
    content = Column(Text)
    ai_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatroomLog(Base):
    __tablename__ = "chatroom_logs"

    id = Column(Integer, primary_key=True)
    role = Column(String(10))       # "user" | "ai"
    ai_name=Column(String(50), nullable=True)
    chatroom_id = Column(String(100))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)