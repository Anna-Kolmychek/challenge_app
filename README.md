# Challenge App

## Описание:
MVP Backend-приложения.

## Как работать с проектом локально:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Anna-Kolmychek/challenge_app.git
```
ИЛИ
```
git clone https://github.com/Anna-Kolmychek/challenge_app.git
```
И
```
cd challenge_app
```

Создать и активировать виртуальное окружение:
```
python -m venv venv
```
```
venv\Scripts\activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции
```
python manage.py makemigrations
python manage.py migrate
```

Загрузить тестовые данные (пользователь с данными 111, 111)
```
python manage.py create_users
python manage.py create_challenges
python manage.py create_progress
```

Запустить локальный сервер Django:
```
python manage.py runserver
```

После запуска сервера документация к API и примеры запросов будут доступны по ссылкам:
http://127.0.0.1:8000/redoc/ и http://127.0.0.1:8000/swagger/
