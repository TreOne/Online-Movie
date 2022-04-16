CREATE SCHEMA IF NOT EXISTS test_schema;
CREATE TABLE IF NOT EXISTS test_schema.movie_watches
(
    MovieID       UUID,
    UserID        UUID,
    ViewDate      DATE,
    ViewTimestamp INT
);
CREATE INDEX movie_watches_movie_user_idx ON test_schema.movie_watches (MovieID, UserID);
