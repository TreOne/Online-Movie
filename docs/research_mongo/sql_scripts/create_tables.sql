BEGIN;
--
-- Пользовательские закладки
--
CREATE TABLE IF NOT EXISTS user_bookmarks
(
    _id         SERIAL                   PRIMARY KEY,
    user_id     uuid                     NOT NULL,
    bookmarks   VARCHAR(255)             NOT NULL
);
create index user_bookmarks_user_id_idx
    on user_bookmarks (user_id);
--
-- Кинопроизведения
--
CREATE TABLE IF NOT EXISTS movies
(
    _id             uuid                     NOT NULL PRIMARY KEY,
    rating          INTEGER                  NOT NULL,
    scores_quantity INTEGER                  NOT NULL,
    scores_amount   INTEGER                  NOT NULL
);
create index movies_rating_idx
    on movies (rating);
--
-- Рецензии
--
CREATE TABLE IF NOT EXISTS reviews
(
    _id             uuid                     NOT NULL PRIMARY KEY,
    movie_id        VARCHAR(255)             NOT NULL,
    user_id         VARCHAR(255)             NOT NULL,
    pub_date        TIMESTAMP WITH TIME ZONE NOT NULL,
    text            TEXT                     NOT NULL,
    movies_score_id VARCHAR(255)             NOT NULL,
    rating          INTEGER                  NOT NULL,
    scores_quantity INTEGER                  NOT NULL,
    scores_amount   INTEGER                  NOT NULL
);
create index reviews_rating_idx
    on reviews (rating);
create index reviews_pub_date_idx
    on reviews (pub_date);
create index reviews_movie_id_idx
    on reviews (movie_id);
--
-- Оценки фильмов
--
CREATE TABLE IF NOT EXISTS movie_scores
(
    _id        uuid                     NOT NULL PRIMARY KEY,
    movie_id   uuid             NOT NULL,
    user_id    VARCHAR(255)             NOT NULL,
    score      INTEGER                  NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies (_id) ON DELETE CASCADE

);
create index movie_scores_user_id_idx
    on movie_scores (user_id);
create index movie_scores_score_idx
    on movie_scores (score);
create index movie_scores_movie_id_idx
    on movie_scores (movie_id);
--
-- Оценки рецензий
--
CREATE TABLE IF NOT EXISTS review_scores
(
    _id        uuid                     NOT NULL PRIMARY KEY,
    review_id  uuid                     NOT NULL,
    user_id    VARCHAR(255)             NOT NULL,
    score      INTEGER                  NOT NULL,
    FOREIGN KEY (review_id) REFERENCES reviews (_id) ON DELETE CASCADE
);
create index review_scores_user_id_idx
    on review_scores (user_id);
create index review_scores_score_idx
    on review_scores (score);
create index review_scores_review_id_idx
    on review_scores (review_id);

COMMIT;