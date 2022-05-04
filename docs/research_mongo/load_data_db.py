from research_mongo.generate_data import (
    upload_to_movies_and_reviews,
    upload_to_movies_and_reviews_postgres,
    upload_to_user_bookmarks,
    upload_to_user_bookmarks_postgres,
)
from research_mongo.tests import check_count_in_tables
from research_mongo.tests_postgres import (
    check_count_in_tables as check_count_in_tables_postgres,
)

if __name__ == '__main__':
    # Mongo
    upload_to_user_bookmarks()
    upload_to_movies_and_reviews()
    check_count_in_tables()
    # Postgres
    upload_to_user_bookmarks_postgres()
    upload_to_movies_and_reviews_postgres()
    check_count_in_tables_postgres()
