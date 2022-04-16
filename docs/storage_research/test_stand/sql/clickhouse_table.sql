CREATE TABLE IF NOT EXISTS movie_watches
(
	MovieID UUID,
	UserID UUID,
    ViewDate Date,
    ViewTimestamp UInt16
)
ENGINE = MergeTree()
ORDER BY (MovieID, UserID);
