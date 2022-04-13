CREATE TABLE movie_watches
(
	MovieID UUID,
	UserID UUID,
    ViewDate Date,
    ViewTimestamp UInt16
)
ENGINE = ReplacingMergeTree()
ORDER BY (MovieID, UserID)
PARTITION BY toYYYYMM(ViewDate);
