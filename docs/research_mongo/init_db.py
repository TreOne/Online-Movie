import config
import sqlalchemy as db_alchemy
from pymongo import MongoClient
from research_mongo.config import DB_NAME, MONGO_HOST, MONGO_PORT
from sqlalchemy.orm import sessionmaker


class MongoDB:

    client = MongoClient(MONGO_HOST, MONGO_PORT)
    mongo_db = client.get_database(DB_NAME)

    USER_BOOKMARKS = mongo_db.get_collection('user_bookmarks')
    MOVIE_SCORES = mongo_db.get_collection('movie_scores')
    MOVIES = mongo_db.get_collection('movies')
    REVIEWS = mongo_db.get_collection('reviews')
    REVIEW_SCORES = mongo_db.get_collection('review_scores')


class PostgresDB:

    def __init__(self):
        self.db_string = f'postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@' \
                         f'{config.POSTGRES_HOST}:5432/{config.POSTGRES_DB}'

    def postgres_db(self):
        engine = db_alchemy.create_engine(self.db_string, pool_pre_ping=True, pool_recycle=5000, echo=False)
        session = sessionmaker(bind=engine, autocommit=True)
        return session()
