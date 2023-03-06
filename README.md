# YaMDb API

### Описание проекта:

Проект YaMDb собирает отзывы пользователей на произведения, позволяет ставить произведениям оценку и комментировать чужие отзывы.

Произведения делятся на категории и на жанры. Список произведений, категорий и жанров может быть расширен администратором.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Полный список запросов и эндпоинтов описан в документации ReDoc, доступна после запуска проекта по адресу:
```
http://localhost/redoc/
```

### Как запустить проект:
Клонировать репозиторий, перейти в директорию с проектом:

```
git@github.com:ApriCotBrain/infra_sp2.git
```

Скачать образ и сохранить его локально:

```
docker pull olgamelikhova2023/yamdb:v1
```

Запустить образ:

```
docker run olgamelikhova2023/yamdb:v1
```

В директории infra/ создать файл .env и заполнить по шаблону:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

Запустить контейнеры:

```
docker-compose up -d --build 
```

Выполнить по очереди команды:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

Проект доступен по адресу:

```
http://localhost/
```

### Авторизация пользователей:
Для получения доступа необходимо создать пользователя отправив POST запрос на эндпоинт ```/api/v1/auth/signup/``` username и email

Запрос:
```
{
"email": "string",
"username": "string"
}
```
После этого на email придет код подтверждения, который вместе с username необходимо отправить POST запросом на эндпоинт```/api/v1/auth/token/```

Запрос:
```
{
"username": "string",
"confirmation_code": "string"
}
```
Ответ:
```
{
"access": "string"
}
```
Полученный токен используется для авторизации

Для просмотра и изменения своих данных используйте эндпоинт ```/api/v1/users/me/```

### Примеры запросов к API:

Получение списка всех категорий:

```
http://127.0.0.1:8000/api/v1/categories/
```
Получение списка всех жанров:

```
http://127.0.0.1:8000/api/v1/genres/
```

Получение списка всех произведений:

```
http://127.0.0.1:8000/api/v1/titles/
```


# Авторы:
```
https://github.com/vvych - Никита Фелькер Тим Лид (Auth/Users)
```
```
https://github.com/ApriCotBrain - Ольга Мелихова (Categories/Genres/Titles)
```
```
https://github.com/Wartherio - Никита Торбин (Review/Comments)
```
