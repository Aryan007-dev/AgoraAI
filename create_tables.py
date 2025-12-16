from database import engine, Base
from models import ChatLog

Base.metadata.create_all(bind=engine)

