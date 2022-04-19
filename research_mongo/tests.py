import random

from pymongo import DESCENDING
from research_mongo.generate_data import (
    get_random_field,
    benchmark,
    get_uuid,
    generate_movie_scores,
    get_random_date,
    generate_review_scores,
)
from research_mongo.init_db import USER_BOOKMARKS, MOVIE_SCORES, MOVIES, REVIEWS, REVIEW_SCORES
from research_mongo.init_db import db
from research_mongo.config import BENCHMARK_ITERATIONS

USER_ID = get_random_field(db, "user_bookmarks")
MOVIE_ID = get_random_field(db, "movie_scores", "movie_id")
# MOVIE_ID = "3c66a837-1058-4b1d-94ff-84767afd7584"
REVIEW_ID = get_random_field(db, "reviews")

def check_add():
#     movie_scores = [a for a in MOVIE_SCORES.find({})]
#     movies = [b for b in MOVIES.find({})]
#     reviews = [c for c in REVIEWS.find({})]
#     review_scores = [d for d in REVIEW_SCORES.find({})]
#     a = MOVIE_SCORES.find_one({"user_id": user_id})
    MOVIE_ID = "3c66a837-1058-4b1d-94ff-84767afd7584"
    b = MOVIES.find_one({"_id": MOVIE_ID})
    a = 5
#     bb = MOVIE_SCORES.find({"_id": {"$in": b.get("scores")}})
#     bbb = list(bb)
#     c = MOVIE_SCORES.find_one({"_id": b.get("scores")[0]})
#     c = REVIEWS.find_one({"_id": review_id})
#     a = REVIEW_SCORES.find_one({"review_id": REVIEW_ID})
#     c = REVIEWS.find_one({"_id": REVIEW_ID})
    return "test"

# check_add()
def check_count_in_tables():
    print("USER_BOOKMARKS - ", USER_BOOKMARKS.count_documents({}))
    print("MOVIE_SCORES - ", MOVIE_SCORES.count_documents({}))
    print("MOVIES - ", MOVIES.count_documents({}))
    print("REVIEWS - ", REVIEWS.count_documents({}))
    print("REVIEW_SCORES - ", REVIEW_SCORES.count_documents({}))


@benchmark(BENCHMARK_ITERATIONS)
def test_get_user_bookmarks():
    user_id = random.choice(USER_ID)
    query = {"_id": user_id}
    user = USER_BOOKMARKS.find_one(query)
    return len(user.get("bookmarks"))

# Список оценок пользователя
@benchmark(BENCHMARK_ITERATIONS)
def test_get_list_user_scores():
    user_id = random.choice(USER_ID)
    query = {"user_id": user_id}
    movies_for_user = MOVIE_SCORES.find(query)
    movies = [movie for movie in movies_for_user]
    return movies


# Количество лайков у фильма
@benchmark(BENCHMARK_ITERATIONS)
def test_get_list_movie_scores():
    movie_id = random.choice(MOVIE_ID)
    query = {"_id": movie_id, "score": {"$gte": 5}}
    good_scores = MOVIE_SCORES.find(query)
    scores = [score for score in good_scores]
    return len(scores)


# Средняя пользовательская оценка фильмов
@benchmark(BENCHMARK_ITERATIONS)
def test_get_rating_movie():
    movie_id = random.choice(MOVIE_ID)
    query = {"_id": movie_id}
    rating = MOVIES.find_one(query)
    return rating


# Фильмы отсортированные по популярности
@benchmark(BENCHMARK_ITERATIONS)
def test_get_popular_movies():
    movies = MOVIES.find().sort("rating", DESCENDING).limit(100)
    movies = [movie for movie in movies]
    return movies

# Список популярных рецензий по фильму
@benchmark(BENCHMARK_ITERATIONS)
def test_get_popular_reviews_for_movie():
    movie_id = random.choice(MOVIE_ID)
    query = {"movie_id": movie_id}
    reviews = REVIEWS.find(query).sort("rating", DESCENDING).limit(100)
    review_ids = [review.get("_id") for review in reviews]
    return review_ids


# Список рецензий фильма от новых к старым
@benchmark(BENCHMARK_ITERATIONS)
def test_get_movies_with_new_reviews():
    movie_id = random.choice(MOVIE_ID)
    query = {"movie_id": movie_id}
    reviews = REVIEWS.find(query).sort("pub_date", DESCENDING).limit(100)
    reviews = [review for review in reviews]
    return reviews


# список положительных рецензий
@benchmark(BENCHMARK_ITERATIONS)
def test_get_good_reviews():
    reviews = REVIEW_SCORES.find({"score": {"$gte": 5}}).limit(100)
    reviews = [review for review in reviews]
    return reviews


# Добавить фильм в закладку к юзеру
@benchmark(BENCHMARK_ITERATIONS)
def test_add_bookmark_to_user():
    movie_id = get_uuid()
    user_id = random.choice(USER_ID)
    user = USER_BOOKMARKS.update_one(
        {"_id": user_id}, {"$addToSet": {"bookmarks": movie_id}}
    )
    print(f"В закладки добавлен фильм - {movie_id} для пользователя - {user_id}")
    return user


# Добавить оценку фильму, обновить рейтинг фильма
@benchmark(BENCHMARK_ITERATIONS)
def test_add_score_to_movie():
    user_id = get_uuid()
    movie_id = random.choice(MOVIE_ID)
    score = generate_movie_scores(user_id, movie_id)
    MOVIE_SCORES.insert_one(score)

    movie = MOVIES.find_one({"_id": movie_id})
    new_score = score.get("score")
    old_scores_amount = movie.get("scores_amount")
    scores_quantity = movie.get("scores_quantity")
    new_rating = ((old_scores_amount + new_score) / (scores_quantity + 1))

    MOVIES.update_one(
        {"_id": movie_id, "scores": {"$ne": score.get("_id")}},
        {
            "$push": {"scores": score.get("_id")},
            "$inc": {"scores_quantity": 1, "scores_amount": new_score},
            "$set": {"rating": int(new_rating)},
        },
    )

    print(f"Фильму - {movie_id} поставлена новая оценка от пользователя - {user_id}")
    return movie

# Добавить рецензию к фильму, обновить рецензии у фильмов
@benchmark(BENCHMARK_ITERATIONS)
def test_add_review_to_movie():
    user_id = get_uuid()
    review_id = get_uuid()
    movie_id = random.choice(MOVIE_ID)
    score = generate_movie_scores(user_id, movie_id)
    MOVIE_SCORES.insert_one(score)

    review = {
        "_id": review_id,
        "movie_id": movie_id,
        "user_id": USER_ID,
        "pub_date": get_random_date(),
        "text": "Test duration add review to movie",
        "movies_score_id": score.get("_id"),
        "rating": 0,
        "scores_quantity": 0,
        "scores": 0,
    }

    movie = MOVIES.find_one({"_id": movie_id})
    new_score = score.get("score")
    old_scores_amount = movie.get("scores_amount")
    scores_quantity = movie.get("scores_quantity")
    new_rating = ((old_scores_amount + new_score) / (scores_quantity + 1))

    MOVIES.update_one(
        {"_id": movie_id, "scores": {"$ne": score.get("_id")}},
        {
            "$push": {"scores": score.get("_id"), "reviews": review.get("_id")},
            "$inc": {"scores_quantity": 1, "scores_amount": new_score},
            "$set": {"rating": int(new_rating)},
        })

    REVIEWS.insert_one(review)
    print(
        f"Фильму - {movie_id} поставлена новая оценка от пользователя - {user_id}, и добавлена"
        f"рецензия {review_id}"
    )
    return movie


# Добавить оценку ревью
@benchmark(BENCHMARK_ITERATIONS)
def test_add_score_to_review():
    review_id = random.choice(REVIEW_ID)
    score = generate_review_scores(review_id)
    user_id = score.get("user_id")

    REVIEW_SCORES.insert_one(score)

    review = REVIEWS.find_one({"_id": review_id})
    new_score = score.get("score")
    old_scores_amount = review.get("scores_amount")
    scores_quantity = review.get("scores_quantity")
    new_rating = ((old_scores_amount + new_score) / (scores_quantity + 1))

    REVIEWS.update_one(
        {"_id": review_id, "scores": {"$ne": score.get("_id")}},
        {
            "$push": {"scores": score.get("_id")},
            "$inc": {"scores_quantity": 1, "scores_amount": new_score},
            "$set": {"rating": int(new_rating)},
        },
    )

    print(f"Рецензии - {review_id} поставлена новая оценка от пользователя - {user_id}")
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

@benchmark(BENCHMARK_ITERATIONS)
def test_get_list_movies_scores():
    movies_for_user = MOVIE_SCORES.aggregate([{"$match": {"movie_id": MOVIE_ID}},
                                              {"$group": {"_id": "$movie_id", "rating": {"$avg": "$score"},
                                                          "scores_quantity": {"$count": {}}}}])
    movies = [movie for movie in movies_for_user]
    return movies


@benchmark(BENCHMARK_ITERATIONS)
def test_add(movie_id):
    agg_movie_scores = MOVIE_SCORES.aggregate([{"$match": {"movie_id": movie_id}},
                                              {"$group": {"_id": "$movie_id", "rating": {"$avg": "$score"},
                                                          "scores_quantity": {"$count": {}}}}])

    movies = list(agg_movie_scores)
    MOVIES.update_one(
        {"_id": movie_id},
        {
            "$set": {"rating": movies[0].get("rating"),
                     "scores_quantity": movies[0].get("scores_quantity")},
        },
    )
    b = MOVIES.find_one({"_id": movie_id})
    print("movie - ", b)
    return b


# Добавить оценку фильму, обновить рейтинг фильма
@benchmark(BENCHMARK_ITERATIONS)
def test_add_score_to_movie1():
    user_id = get_uuid()
    score = generate_movie_scores(user_id, MOVIE_ID)
    MOVIE_SCORES.insert_one(score)

    agg_movie_scores = MOVIE_SCORES.aggregate([{"$match": {"movie_id": MOVIE_ID}},
                                               {"$group": {"_id": "$movie_id", "rating": {"$avg": "$score"},
                                                           "scores_quantity": {"$count": {}}}}])
    movie = list(agg_movie_scores)
    MOVIES.update_one(
        {"_id": MOVIE_ID},
        {
            "$set": {"rating": movie[0].get("rating"),
                     "scores_quantity": movie[0].get("scores_quantity")},
        },
    )
    print(f"Фильму - {MOVIE_ID} поставлена новая оценка от пользователя - {user_id}")
    return movie

















