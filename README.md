# REST API для сервиса YaMDb

![example event parameter](https://github.com/learies/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

REST API проект для сервиса YaMDb — собирает отзывы пользователей на произведения.
Произведения делятся на категории. Список категорий может быть расширен администратором.

Пример категорий:
- Фильмы;
- Книги;
- Музыка;
- и другие ...

Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

Сами произведения в YaMDb не хранятся

## Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

## Регистрация новых пользователей
1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт `/api/v1/auth/signup/`
2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

## Ресурсы API YaMDb
- **auth**: аутентификация.
- **users**: пользователи.
- **titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- **categories**: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- **reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.
- **comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

# Связанные данные и каскадное удаление
- При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
- При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
- При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.
- При удалении объекта категории Category не нужно удалять связанные с этой категорией произведения.
- При удалении объекта жанра Genre не нужно удалять связанные с этим жанром произведения.

## Установка

### Клонирование репозитория
```bash
$ git clone git@github.com:learies/yamdb_final.git
```
### Создать виртуальное окружение
```bash
$ python3 -m venv venv
```
### Перейти в директорию проекта
```bash
$ cd api_yamdb/
```
### Установить зависимости [pip](https://pip.pypa.io/en/stable/)
```bash
$ pip install -r requirements.txt
```
### Создать миграции
```bash
$ python manage.py makemigrations
```
```bash
$ python manage.py migrate
```
### Заполнить db данными
```bash
$ python script_db.py
```
### Запустить сервер
```bash
$ python manage.py migrate
```

## cocker-compose
### Перейти в директорию с файлом docker-compose.yaml:
```bash
$ cd infra
```
### Запустить
```bash
$ docker-compose up -d --build
```

### Выполнить миграции
```bash
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate
```
### Создаем суперпользователя
```bash
$ docker-compose exec web python manage.py createsuperuser 
```
### Собрать статику
```bash
$ docker-compose exec web python manage.py collectstatic --no-input
```
### Остановить контейнеры
```bash
$ docker-compose down -v
```
## Документация
```
http://127.0.0.1:8000/redoc/
```
или
```
http://51.250.27.161/redoc/
```
## License
Free
