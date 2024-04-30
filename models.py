from sqlalchemy import create_engine, Column, Integer, String, Boolean,ForeignKey,DateTime
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker,relationship
from datetime import datetime


url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="admin",    
    host="localhost",
    database="postgres",
    port=5432
)
engine = create_engine(url)
Session = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    sender = Column(String)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_system_message = Column(Boolean, default=False)
    chat = relationship("Chat", back_populates="messages")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(engine)
