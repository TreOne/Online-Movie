## Базовый образ для сборки
FROM python:3.9.10-slim as builder

WORKDIR /usr/src/app

# Запрещаем Python писать файлы .pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Запрещает Python буферизовать stdout и stderr
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc netcat dos2unix && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем точку входа
COPY /deploy/auth/entrypoint.dev.sh .
# Fix права на выполнение (для пользователей unix систем)
RUN ["chmod", "+x", "entrypoint.dev.sh"]
# Fix окончания строк (для пользователей win систем)
RUN dos2unix entrypoint.dev.sh

# Проверка оформления кода
RUN pip install --upgrade pip
RUN pip install flake8
COPY /src/auth_api .
RUN flake8 --ignore=W503,E501,F401,E231 .

# Установка зависимостей
COPY /deploy/auth/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


## СБОРКА
FROM python:3.9.10-slim

# Создаем не root пользователя для проекта
RUN mkdir -p /home/app
RUN adduser --system --group app

# Создаем необходимые директории
ENV HOME=/home/app
ENV APP_HOME=/home/app/src
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install --no-install-recommends -y netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем точку входа
COPY --from=builder /usr/src/app/entrypoint.dev.sh $HOME

# Копируем файлы проекта
COPY /src/auth_api $APP_HOME/auth_api
COPY /src/auth_api/migrations $APP_HOME/migrations

# Изменяем владельца файлов на app
RUN chown -R app:app $APP_HOME

# Переключаемся на пользователя app
USER app

# Запускаем точку входа
ENTRYPOINT ["/home/app/entrypoint.dev.sh"]


#
#
#
#FROM python:3.9.10-bullseye
#
#WORKDIR /app
#
#RUN pip install --upgrade pip
#COPY /deploy/auth/requirements.txt ./
#RUN pip install -r requirements.txt
#
#COPY /src/auth_api/ auth_api/
#
#EXPOSE 5000
