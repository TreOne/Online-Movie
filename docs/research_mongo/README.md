### Запуск тестов
Поднять контейнеры с Монго:
```shell
docker-compose up -d --build
docker-compose exec mongocfg1 sh -c "mongosh <  /scripts/config_server.js"
docker-compose exec mongors1n1 sh -c "mongosh < /scripts/shard_1.js"
docker-compose exec mongors2n1 sh -c "mongosh  < /scripts/shard_2.js"
docker-compose exec mongos1 sh -c "mongosh < /scripts/router.js"
docker-compose exec mongos1 sh -c "mongosh < /scripts/init_db.js"
```
- В config.py установить значения переменных, для генерации необходимого количества данных
- Запустить скрипт генерации и загрузки данных в Монго - load_data_db.py
- Запустить скрипт выполнения тестов - test_runner.py

### Задачи исследования
Измерить скорость добавления и чтения данных хранилища при следующих требованиях:
- количество пользователей: 200000
- количество фильмов: 10000
- максимальное время ответа: 200мс

### Выводы исследования
MongoDB удовлетворяет требуемым показателям производительности и может быть использовано
для хранения пользовательских оценок и отзывов.

### Структура данных
Данных в БД Mongo:
	Пользователи с закладками фильмов -  215 000
	(у каждого пользователя по 50 фильмов в закладках)
	Оценки фильмов -  9 805 157
	Фильмы -  10 000
	(из них: у 1 000 по 2 000 оценок
        	 у 1 000 по 4 000 оценок
	 	     у 4 000 по 700 оценок
	 	     у 4 000 по 100 оценок
	Рецензии -  354 200
	Оценки рецензий -  11 341 642

Данных в БД Postgres:
	Пользователи с закладками фильмов -  215 000
	Оценки фильмов -  9 805 157
	Фильмы -  10 000
	Рецензии -  354 200
	Оценки рецензий -  11 341 642

БД разделена на следующие коллекции:

- **user_bookmarks**
    - схема данных:

            {
                "_id": <uuid_string>,
                "bookmarks": [<uuid_string>, ...]
            }
    - ключ шардирования: **_id**

- **movie_scores**
    - схема данных:

            {
                "_id": <uuid_string>,
                "movie_id": <uuid_string>,
                "user_id": <uuid_string>,
                "score": <integer>
            }
    - ключ шардирования: **movie_id**

- **movies**
    - схема данных:

            {
                "_id": <uuid_string>,
                "rating": <integer>,
                "scores_quality": <integer>
                "scores_amount": <integer>
                "scores": [<uuid_string>, ...]
                "reviews": [<uuid_string>, ...]
            }
    - ключ шардирования: **_id**

- **reviews**
    - схема данных:

            {
                "_id": <uuid_string>,
                "user_id": <uuid_string>,
                "movie_id": <uuid_string>,
                "pub_date": <datetime>,
                "text": <string>,
                "movie_score_id": <uuid_string>,
                "rating": <integer>,
                "scores_quality": <integer>,
                "scores_amount": <integer>,
                "scores": [<uuid_string>, ...]
            }
    - ключ шардирования: **movie_id**

- **review_scores**
    - схема данных:

            {
                "_id": <uuid_string>,
                "review_id": <uuid_string>,
                "user_id": <uuid_string>,
                "score": <integer>
            }
    - ключ шардирования: **review_id**

### Результаты тестирования
- итераций теста: 20

#### Операции чтения

| получение                                     | Mongo, ср. время, с | Postgres, ср. время, с |
|-----------------------------------------------|---------------------|------------------------|
| закладок пользователя                         | 0.0027              | 0.0068                 |
| фильмов с оценками пользователя               | 0.0028              | 0.0072                 |
| всех оценок фильма                            | 0.0024              | 0.0187                 |
| рейтинга фильмов                              | 0.0074              | 0.0049                 |
| топ 100 самых популярных фильмов              | 0.0638              | 0.0064                 |
| популярных рецензий по фильму                 | 0.0133              | 0.0079                 |
| рецензии фильма отсортированные по дате публ. | 0.0141              | 0.0166                 |
| списка положительных рецензий                 | 0.0036              | 0.0077                 |
            |

#### Операции записи

| добавление            | Mongo, ср. время, с |  Postgres, ср. время, с |
|-----------------------|---------------------|---------------------- --|
| закладки пользователю | 0.0059              | 0.0123                  |
| рецензии к фильму     | 0.0329              | 0.0289                  |
| оценки к рецензии     | 0.0299              | 0.0259                  |
| оценки к фильму       | 0.0166              | 0.0237                  |
