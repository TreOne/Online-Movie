FROM python:3.9.10-bullseye

WORKDIR /app

RUN pip install --upgrade pip
COPY /deploy/auth/requirements.txt ./
RUN pip install -r requirements.txt

COPY /src/auth_api/ auth_api/

EXPOSE 5000