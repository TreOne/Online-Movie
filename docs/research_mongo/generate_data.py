import datetime
import functools
import random
import uuid
from time import time

from init_db import PostgresDB
from models import Movies, MovieScores, Reviews, ReviewScores, UserBookmarks
from research_mongo.config import (
    BOOKMARKS_PER_USER,
    MAX_RATING,
    MAX_REVIEW_SCORE,
    MIN_RATING,
    MOVIES_COUNT,
    REVIEWS_FOR_MOVIE,
    SCORES_FOR_MOVIE,
    USERS_COUNT,
)
from research_mongo.init_db import MongoDB

USER_BOOKMARKS = MongoDB.USER_BOOKMARKS
MOVIE_SCORES = MongoDB.MOVIE_SCORES
MOVIES = MongoDB.MOVIES
REVIEWS = MongoDB.REVIEWS
REVIEW_SCORES = MongoDB.REVIEW_SCORES


def get_uuid():
    return str(uuid.uuid4())


USER_IDS = [get_uuid() for _ in range(USERS_COUNT)]
MOVIES_IDS = [get_uuid() for _ in range(MOVIES_COUNT)]


def get_random_field(mongo_db, collection, name='_id'):
    try:
        return [
            doc.get(name)
            for doc in mongo_db.get_collection(collection).aggregate(
                [{'$sample': {'size': 50}}],
            )
        ]
    except StopIteration:
        print('Коллекция пустая')


def get_random_date():
    day = random.randint(0, 600)
    hour = random.randint(0, 23)
    minut = random.randint(0, 59)
    random_date = datetime.datetime.utcnow() - datetime.timedelta(
        days=day, hours=hour, minutes=minut,
    )
    return random_date.strftime('%Y/%m/%d %I:%M')


def generate_user_bookmarks():
    for user_id in USER_IDS:
        yield {
            '_id': user_id,
            'bookmarks': [
                movie_id for movie_id in random.sample(MOVIES_IDS, BOOKMARKS_PER_USER)
            ],
        }


def generate_movie_scores(user_id, movie_id):
    score = {
        '_id': get_uuid(),
        'movie_id': movie_id,
        'user_id': user_id,
        'score': random.randint(MIN_RATING, MAX_RATING),
    }
    return score


def generate_movie(movie_id, movies_scores, reviews):
    scores_quantity = len(movies_scores)
    scores_amount = sum(mscore.get('score') for mscore in movies_scores)
    rating = int(scores_amount / scores_quantity)
    movie = {
        '_id': movie_id,
        'rating': rating,
        'scores_quantity': scores_quantity,
        'scores_amount': scores_amount,
        'scores': [mscore.get('_id') for mscore in movies_scores],
        'reviews': [review.get('_id') for review in reviews],
    }
    return movie


def generate_review_scores(review_id):
    review_score = {
        '_id': get_uuid(),
        'review_id': review_id,
        'user_id': random.choice(USER_IDS),
        'score': random.randint(MIN_RATING, MAX_RATING),
    }
    return review_score


def generate_review(user_id, movie_id, movies_score_id):
    review_id = get_uuid()
    scores_quantity = random.randint(1, MAX_REVIEW_SCORE)
    scores = [generate_review_scores(review_id) for _ in range(scores_quantity)]
    scores_amount = sum(score.get('score') for score in scores)
    rating = int(scores_amount / scores_quantity)
    review = {
        '_id': review_id,
        'movie_id': movie_id,
        'user_id': user_id,
        'pub_date': get_random_date(),
        'text': 'Research storage selection study',
        'movies_score_id': movies_score_id,
        'rating': rating,
        'scores_quantity': scores_quantity,
        'scores_amount': scores_amount,
        'scores': [score.get('_id') for score in scores],
    }
    return review, scores


def prepare_movie_and_reviews(movie_id):
    user_ids = random.sample(USER_IDS, SCORES_FOR_MOVIE)
    movie_scores = []
    reviews = []
    review_scores = []
    for idx, user_id in enumerate(user_ids):
        ms = generate_movie_scores(user_id, movie_id)
        movie_scores.append(ms)
        if idx < REVIEWS_FOR_MOVIE:
            review, rs = generate_review(user_id, movie_id, ms.get('_id'))
            reviews.append(review)
            review_scores.extend(rs)

    movie = generate_movie(movie_id, movie_scores, reviews)

    return movie_scores, movie, reviews, review_scores


def upload_to_user_bookmarks():
    print(f'Старт загрузки данных в таблицу закладок юзера')
    USER_BOOKMARKS.insert_many(generate_user_bookmarks(), ordered=False)
    print(f'Загрузка данных в таблицу закладок юзера завершена')


def upload_to_movies_and_reviews():
    for idx, movie_id in enumerate(MOVIES_IDS):

        movie_scores, movie, reviews, review_scores = prepare_movie_and_reviews(
            movie_id,
        )

        MOVIE_SCORES.insert_many(movie_scores, ordered=False)

        MOVIES.insert_one(movie)

        REVIEWS.insert_many(reviews, ordered=False)

        REVIEW_SCORES.insert_many(review_scores, ordered=False)

        if idx % 100 == 0:
            print(f'Загружено фильмов: {idx + 100} шт')


def benchmark(iteration):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            iterations_time = []
            for i in range(iteration):
                start = time()
                func(*args)
                finish = time() - start
                iterations_time.append(finish)
            avg_time = sum(iterations_time) / iteration

            print(f'Название теста - {func.__name__}')
            print(f'Количество итераций - {iteration}')
            print(f'Средняя продолжительность запроса - {avg_time:.4f} c\n')

        return inner

    return decorator


def upload_to_user_bookmarks_postgres():
    print(f'Старт загрузки данных в таблицу закладок юзера')
    postgres_db = PostgresDB().postgres_db()
    user_bookmarks = []
    quan_users = len(USER_IDS)
    for idx, user in enumerate(generate_user_bookmarks()):
        user_id, bookmarks = user.values()
        for bookmark in bookmarks:
            row = UserBookmarks(user_id=user_id, bookmarks=bookmark)
            user_bookmarks.append(row)
        if len(user_bookmarks) % 100 == 0 or quan_users == idx + 1:
            postgres_db.bulk_save_objects(user_bookmarks)
            user_bookmarks.clear()
    print(f'Загрузка данных в таблицу закладок юзера завершена')


def upload_to_movies_and_reviews_postgres():
    postgres_db = PostgresDB().postgres_db()
    movie_scores_for_bulk, movie_bulk, reviews_bulk, review_scores_bulk = [], [], [], []
    quan_movies = len(MOVIES_IDS)
    for idx, movie_id in enumerate(MOVIES_IDS):
        movie_scores, movie, reviews, review_scores = prepare_movie_and_reviews(movie_id)
        movie.pop('scores')
        movie.pop('reviews')
        for review in reviews:
            review.pop('scores')
        movie_scores_obj = [MovieScores(**ms) for ms in movie_scores]
        movie_obj = Movies(**movie)
        reviews_obj = [Reviews(**rw) for rw in reviews]
        review_scores_obj = [ReviewScores(**rws) for rws in review_scores]

        movie_scores_for_bulk.extend(movie_scores_obj)
        movie_bulk.append(movie_obj)
        reviews_bulk.extend(reviews_obj)
        review_scores_bulk.extend(review_scores_obj)
        if idx % 20 == 0 or quan_movies == idx + 1:
            postgres_db.bulk_save_objects(movie_bulk)
            postgres_db.bulk_save_objects(movie_scores_for_bulk)
            postgres_db.bulk_save_objects(reviews_bulk)
            postgres_db.bulk_save_objects(review_scores_bulk)
            postgres_db.query(Movies).first()
            movie_scores_for_bulk, movie_bulk, reviews_bulk, review_scores_bulk = [], [], [], []
        if idx % 100 == 0:
            print(f'Загружено фильмов: {idx} шт')
