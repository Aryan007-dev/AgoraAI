from sqlalchemy.orm import Session
from models import MessageLog

def log_message(db: Session, sender: str, agent_name: str, content: str|None=None):
    """Logs a message to the database."""
    message = MessageLog(sender=sender, agent=agent_name, content=content)
    db.add(message)
    db.commit()
   