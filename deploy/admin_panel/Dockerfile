## Базовый образ для сборки
FROM python:3.9-slim as builder

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
COPY /deploy/admin_panel/entrypoint.sh .
# Fix права на выполнение (для пользователей unix систем)
RUN ["chmod", "+x", "entrypoint.sh"]
# Fix окончания строк (для пользователей win систем)
RUN dos2unix entrypoint.sh

# Проверка оформления кода
RUN pip install --upgrade pip
RUN pip install flake8
COPY /src/admin_panel .
RUN flake8 --ignore=E501,F401 .

# Установка зависимостей
COPY /deploy/admin_panel/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


## СБОРКА
FROM python:3.9-slim

# Создаем не root пользователя для проекта
RUN mkdir -p /home/app
RUN adduser --system --group app

# Создаем необходимые директории
ENV HOME=/home/app
ENV APP_HOME=/home/app/admin_panel
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install --no-install-recommends -y netcat gettext
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем точку входа
COPY --from=builder /usr/src/app/entrypoint.sh $HOME

# Копируем демо-данные для проекта
COPY /deploy/admin_panel/fixtures.json.gz $HOME

# Копируем файлы проекта
COPY /src/admin_panel $APP_HOME

# Изменяем владельца файлов на app
RUN chown -R app:app $APP_HOME

# Переключаемся на пользователя app
USER app

# Запускаем точку входа
ENTRYPOINT ["/home/app/entrypoint.sh"]
