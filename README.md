### Описание проекта api_yamdb:


Проект YaMDb собирает отзывы пользователей на различные произведения:
* фильмы
* книги
* музыка
_(список категорий может быть расширен администратором)_

Пользователи могут оставлять отзыв и оценку произведению. На базе оценки формируется средний рейтинг произведения.

К отзывам доступны комментарии.

### Пользовательские роли
* **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь (user)** — может читать всё, как и Аноним,
может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/музыке), 
может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии,
редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
* **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/viator3m/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
---
### Регистрация
1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
```
POST localhost:8000/api/v1/signup/
Content-Type: application/json

{
  "username": "example_user",
  "email": "example@example.com"
}
```
2. Сервис YaMDB отправляет письмо с кодом подтверждения `confirmation_code` на указанный адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт 
/api/v1/auth/token/, в ответе на запрос ему приходит `token` (JWT-токен).

Запрос на получение токена
```
POST localhost:8000/api/v1/auth/token/
Content-Type: application/json

{
  "username": "example_user",
  "password": "123456"
}
```
Ответ сервера
```
"token: eyJ0eXAiOiJKV1Q..."
```
Полученный токен используется в заголовке запроса к эндпойнтам требующих авторизации

### Некоторые примеры запросов к API

---
POST-запрос на добавление отзыва
```
POST http://localhost:8000/api/v1/titles/{title_id}/reviews/
Content-Type: application/json
Authorization: Bearer "eyJ0eXAiOi..."

{
    "text": "example review",
    "score": 1
}
```
Пример ответа
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```

POST-запрос на добавление комментария
```
POST http://localhost:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
Content-Type: application/json
Authorization: Bearer "eyJ0eXAiOi..."

{
    "text": "example review",
}
```
Пример ответа
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```

С полной документацией можно ознакомиться по адресу [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

Авторы:
- [Vladimir Kamyshanov](https://github.com/viator3m)
- [Pavel Gavrilenko](https://github.com/pavelGavrilenko)
- [Artem Pavlishev](https://github.com/artemkms)
