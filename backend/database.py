from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

# Create SQLite engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    sender_name = Column(String)
    recipient = Column(String)
    subject = Column(String, index=True)
    body = Column(Text)
    category = Column(String, index=True, default="Uncategorized")
    priority = Column(String, default="Medium")
    received_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    has_action_items = Column(Boolean, default=False)
    action_items = Column(Text)  # JSON string
    sentiment = Column(String)
    

class Prompt(Base):
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    prompt_type = Column(String, index=True)  # categorization, task_extraction, auto_reply
    content = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Draft(Base):
    __tablename__ = "drafts"
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, index=True)
    subject = Column(String)
    body = Column(Text)
    tone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_sent = Column(Boolean, default=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with tables"""
    Base.metadata.create_all(bind=engine)
