from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from utils.logger import Logger

load_dotenv()

logger = Logger()

class DB:
    def __init__(self):
        db_username = os.environ['DB_USERNAME']
        db_password = os.environ['DB_PASSWORD']
        db_host = os.environ['DB_HOST']
        
        engine_str = f"mysql+pymysql://{db_username}:{db_password}@{db_host}"
        self.engine = create_engine(engine_str)
        self.session_maker = sessionmaker(bind=self.engine)

        try:
            self.engine.connect()
            logger.info("Successfully connected to the database")
        except Exception as e:
            logger.error(f"Failed to connect to the database. Error: {e}")
