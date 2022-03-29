## Базовый образ для сборки
FROM python:3.9-slim as builder

WORKDIR /usr/src/app

# Запрещаем Python писать файлы .pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Запрещает Python буферизовать stdout и stderr
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Проверка оформления кода
RUN pip install --upgrade pip
RUN pip install flake8
COPY /src/ps_to_es .
RUN flake8 --ignore=E501,F401 .

# Установка зависимостей
COPY /deploy/ps_to_es/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


## СБОРКА
FROM python:3.9-slim

# Создаем не root пользователя для проекта
RUN mkdir -p /home/app
RUN adduser --system --group app

# Создаем необходимые директории
ENV HOME=/home/app
ENV APP_HOME=/home/app/etl
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Устанавливаем зависимости
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем файлы проекта
COPY /src/ps_to_es $APP_HOME

# Изменяем владельца файлов на app
RUN chown -R app:app $APP_HOME

# Переключаемся на пользователя app
USER app

# Запускаем скрипт
CMD [ "python", "/home/app/etl/main.py" ]
