# pull official base image
FROM python:3.8

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# Создаем таблицы в бд (будут всегда пустыми при каждом новом запуске)
RUN python manage.py makemigrations
RUN python manage.py makemigrations api_deal
RUN python manage.py migrate
RUN mkdir /usr/src/app/static
RUN python manage.py collectstatic --noinput

RUN python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@mal.ru', >
