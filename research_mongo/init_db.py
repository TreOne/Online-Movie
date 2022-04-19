import sqlalchemy as db_alchemy
from pymongo import MongoClient
from sqlalchemy.orm import sessionmaker

import config
from research_mongo.config import (MONGO_PORT, MONGO_HOST, DB_NAME)

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.get_database(DB_NAME)

USER_BOOKMARKS = db.get_collection("user_bookmarks")
MOVIE_SCORES = db.get_collection("movie_scores")
MOVIES = db.get_collection("movies")
REVIEWS = db.get_collection("reviews")
REVIEW_SCORES = db.get_collection("review_scores")


class PostgresDB:

    def __init__(self):
        self.db_string = f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:5432/{config.POSTGRES_DB}"

    def postgres_db(self):
        engine = db_alchemy.create_engine(self.db_string, pool_pre_ping=True, pool_recycle=5000, echo=False)
        session = sessionmaker(bind=engine, autocommit=True)
        return session()
