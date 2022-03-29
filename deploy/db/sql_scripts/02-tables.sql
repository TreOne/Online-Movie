BEGIN;
--
-- Жанры кинопроизведений
--
CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid                     NOT NULL PRIMARY KEY,
    name        VARCHAR(255)             NOT NULL UNIQUE,
    description TEXT                     NULL,
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at  TIMESTAMP WITH TIME ZONE NOT NULL
);

--
-- Персоны (актёры/режисёры/сценаристы)
--
CREATE TABLE IF NOT EXISTS content.person
(
    id         uuid                     NOT NULL PRIMARY KEY,
    full_name  VARCHAR(255)             NOT NULL,
    birth_date DATE                     NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT unique_person UNIQUE(full_name, birth_date)
);

--
-- Кинопроизведения (фильм/сериал)
--
CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid                     NOT NULL PRIMARY KEY,
    title         VARCHAR(255)             NOT NULL,
    description   TEXT                     NULL,
    creation_date DATE                     NULL,
    certificate   TEXT                     NULL,
    file_path     VARCHAR(100)             NULL,
    rating        DOUBLE PRECISION         NULL,
    type          VARCHAR(25)              NOT NULL,
    created_at    TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at    TIMESTAMP WITH TIME ZONE NOT NULL
);

--
-- Связь: Кинопроизведения - Жанры кинопроизведений
--
CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid                     NOT NULL PRIMARY KEY,
    film_work_id uuid                     NOT NULL,
    genre_id     uuid                     NOT NULL,
    created_at   TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE,
    CONSTRAINT unique_film_work_genre_link UNIQUE(film_work_id, genre_id)
);

--
-- Связь: Кинопроизведения - Персоны
--
CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid                     NOT NULL PRIMARY KEY,
    film_work_id uuid                     NOT NULL,
    person_id    uuid                     NOT NULL,
    role         VARCHAR(25)              NOT NULL,
    created_at   TIMESTAMP WITH TIME ZONE NOT NULL,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE,
    CONSTRAINT unique_person_film_work_role UNIQUE(film_work_id, person_id, role)
);

COMMIT;
