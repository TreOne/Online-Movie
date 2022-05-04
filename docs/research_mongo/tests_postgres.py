import random

from pymongo import DESCENDING
from research_mongo.config import BENCHMARK_ITERATIONS
from research_mongo.generate_data import (
    benchmark,
    generate_movie_scores,
    generate_review_scores,
    get_random_date,
    get_random_field,
    get_uuid,
)
from research_mongo.init_db import PostgresDB
from research_mongo.models import (
    Movies,
    MovieScores,
    Reviews,
    ReviewScores,
    UserBookmarks,
)
from sqlalchemy import desc
from sqlalchemy.sql import func

postgres_db = PostgresDB().postgres_db()

USER_ID = [
    str(uuid.user_id) for uuid in postgres_db.query(UserBookmarks.user_id).order_by(func.random()).limit(
        100,
    ).all()
]
MOVIE_ID = [
    str(uuid._id) for uuid in postgres_db.query(Movies._id).order_by(func.random()).limit(
        100,
    ).all()
]
REVIEW_ID = [
    str(uuid._id) for uuid in postgres_db.query(Reviews._id).order_by(func.random()).limit(
        100,
    ).all()
]


def check_count_in_tables():
    print(
        'Пользователей с закладками фильмов - ', postgres_db.query(UserBookmarks).distinct(
            UserBookmarks.user_id,
        ).count(),
    )
    print('Закладок фильмов - ', postgres_db.query(UserBookmarks).count())
    print('Оценок фильмов - ', postgres_db.query(MovieScores).distinct(MovieScores._id).count())
    print('Фильмов - ', postgres_db.query(Movies).distinct(Movies._id).count())
    print('Рецензий - ', postgres_db.query(Reviews).distinct(Reviews._id).count())
    print('Оценок рецензий - ', postgres_db.query(ReviewScores).distinct(ReviewScores._id).count())


@benchmark(BENCHMARK_ITERATIONS)
def test_get_user_bookmarks():
    user_id = random.choice(USER_ID)
    user = postgres_db.query(UserBookmarks.bookmarks).filter(UserBookmarks.user_id == user_id).all()
    return len(user)


# Список оценок пользователя
@benchmark(BENCHMARK_ITERATIONS)
def test_get_list_user_scores():
    user_id = random.choice(USER_ID)
    movies_for_user = postgres_db.query(MovieScores).filter(MovieScores.user_id == user_id).all()
    movies = [movie.__dict__ for movie in movies_for_user]
    return movies


# Количество лайков у фильма
@benchmark(BENCHMARK_ITERATIONS)
def test_get_list_movie_scores():
    movie_id = random.choice(MOVIE_ID)
    good_scores = postgres_db.query(MovieScores).filter(MovieScores.movie_id == movie_id, MovieScores.score >= 5).all()
    scores = [score.__dict__ for score in good_scores]
    return len(scores)


# Средняя пользовательская оценка фильмов
@benchmark(BENCHMARK_ITERATIONS)
def test_get_rating_movie():
    movie_id = random.choice(MOVIE_ID)
    rating = postgres_db.query(Movies.rating).filter(Movies._id == movie_id).scalar()
    return rating


# Фильмы отсортированные по популярности
@benchmark(BENCHMARK_ITERATIONS)
def test_get_popular_movies():
    # movies = MOVIES.find().sort("rating", DESCENDING).limit(100)
    movies = postgres_db.query(Movies).order_by(desc(Movies.rating)).limit(100).all()
    movies = [movie.__dict__ for movie in movies]
    return movies


# Список популярных рецензий по фильму
@benchmark(BENCHMARK_ITERATIONS)
def test_get_popular_reviews_for_movie():
    movie_id = random.choice(MOVIE_ID)
    reviews = postgres_db.query(Reviews).filter(Reviews.movie_id == movie_id).order_by(desc(Reviews.rating)).limit(
        100,
    ).all()
    review_ids = [review.__dict__ for review in reviews]
    return review_ids


# Список рецензий фильма от новых к старым
@benchmark(BENCHMARK_ITERATIONS)
def test_get_movies_with_new_reviews():
    movie_id = random.choice(MOVIE_ID)
    reviews = postgres_db.query(Reviews).filter(Reviews.movie_id == movie_id).order_by(desc(Reviews.pub_date)).limit(
        100,
    ).all()
    review_ids = [review.__dict__ for review in reviews]
    return review_ids


# список положительных рецензий
@benchmark(BENCHMARK_ITERATIONS)
def test_get_good_reviews():
    reviews = postgres_db.query(ReviewScores).filter(ReviewScores.score >= 5).limit(100).all()
    reviews = [review._id for review in reviews]
    return reviews


# Добавить фильм в закладку к юзеру
@benchmark(BENCHMARK_ITERATIONS)
def test_add_bookmark_to_user():
    movie_id = get_uuid()
    user_id = random.choice(USER_ID)
    user = UserBookmarks(user_id=user_id, bookmarks=movie_id)
    postgres_db.add(user)
    postgres_db.query(UserBookmarks.bookmarks).filter(UserBookmarks.bookmarks == movie_id).first()
    print(f'В закладки добавлен фильм - {movie_id} для пользователя - {user_id}')
    return movie_id


# Добавить оценку фильму, обновить рейтинг фильма
@benchmark(BENCHMARK_ITERATIONS)
def test_add_score_to_movie():
    user_id = get_uuid()
    movie_id = random.choice(MOVIE_ID)
    score = MovieScores(**generate_movie_scores(user_id, movie_id))
    postgres_db.add(score)
    movie = postgres_db.query(Movies).filter(Movies._id == movie_id).first()
    new_score = score.score
    scores_quantity = movie.scores_quantity
    scores_amount = movie.scores_amount
    new_rating = (scores_amount + new_score) / (scores_quantity + 1)

    postgres_db.query(Movies).filter(Movies._id == movie_id).update({
        Movies.scores_quantity: (
            scores_quantity + 1
        ), Movies.rating: int(new_rating),
    })

    print(f'Фильму - {movie_id} поставлена новая оценка от пользователя - {user_id}')
    return movie


# Добавить рецензию к фильму, обновить рецензии у фильмов
@benchmark(BENCHMARK_ITERATIONS)
def test_add_review_to_movie():
    user_id = get_uuid()
    review_id = get_uuid()
    movie_id = random.choice(MOVIE_ID)
    score = MovieScores(**generate_movie_scores(user_id, movie_id))
    postgres_db.add(score)

    review = Reviews(
        _id=review_id,
        movie_id=movie_id,
        user_id=user_id,
        pub_date=get_random_date(),
        text='Test duration add review to movie',
        movies_score_id=score._id,
        rating=0,
        scores_quantity=0,
        scores_amount=0,

    )
    postgres_db.add(review)
    movie = postgres_db.query(Movies).filter(Movies._id == movie_id).first()
    new_score = score.score
    scores_quantity = movie.scores_quantity
    scores_amount = movie.scores_amount
    new_rating = (scores_amount + new_score) / (scores_quantity + 1)

    postgres_db.query(Movies).filter(Movies._id == movie_id).update({
        Movies.scores_quantity: (
            scores_quantity + 1
        ), Movies.rating: int(new_rating),
    })

    print(
        f'Фильму - {movie_id} поставлена новая оценка от пользователя - {user_id}, и добавлена'
        f'рецензия {review_id}',
    )
    return movie


# Добавить оценку ревью
@benchmark(BENCHMARK_ITERATIONS)
def test_add_score_to_review():
    review_id = random.choice(REVIEW_ID)
    score = ReviewScores(**generate_review_scores(review_id))
    user_id = score.user_id
    postgres_db.add(score)

    review = postgres_db.query(Reviews).filter(Reviews._id == review_id).first()
    new_score = score.score
    scores_quantity = review.scores_quantity
    scores_amount = review.scores_amount
    new_rating = (scores_amount + new_score) / (scores_quantity + 1)

    postgres_db.query(Reviews).filter(Reviews._id == review_id).update({
        Reviews.scores_quantity: (
            scores_quantity + 1
        ), Reviews.rating: int(new_rating),
    })
    print(f'Рецензии - {review_id} поставлена новая оценка от пользователя - {user_id}')
    return review


read_tests = [
    test_get_user_bookmarks,
    test_get_list_user_scores,
    test_get_list_movie_scores,
    test_get_rating_movie,
    test_get_popular_movies,
    test_get_popular_reviews_for_movie,
    test_get_movies_with_new_reviews,
    test_get_good_reviews,
]

write_tests = [
    test_add_bookmark_to_user,
    test_add_score_to_movie,
    test_add_review_to_movie,
    test_add_score_to_review,
]
