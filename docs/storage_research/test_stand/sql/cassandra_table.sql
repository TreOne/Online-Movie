CREATE KEYSPACE IF NOT EXISTS test_keyspace
    WITH REPLICATION = {
        'class' : 'SimpleStrategy',
        'replication_factor': 1
        };

CREATE TABLE IF NOT EXISTS test_keyspace.movie_watches
(
    id            UUID PRIMARY KEY,
    MovieID       UUID,
    UserID        UUID,
    ViewDate      DATE,
    ViewTimestamp INT
);

CREATE INDEX movie_watches_movie_idx ON test_keyspace.movie_watches (MovieID);
CREATE INDEX movie_watches_user_idx ON test_keyspace.movie_watches (UserID);
