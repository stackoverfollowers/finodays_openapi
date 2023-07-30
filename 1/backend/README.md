# Задание 1. Использование VK API для авторизации

Приложение отдает ссылку на авторизацию и помогает получить данные о пользователе в нашем приложении

Используемые библиотеки: FastApi, pydantic_settings, httpx-oauth, версия Python не ниже 3.10

## Environments

Перед запуском необходимо установить нужные пакеты

```bash
python -m venv/venv
source venv/bin/activate
pip install -r reqiurements.txt
```

(Рабочая директория - `backend/`)

И заполнить файл .env нужными данными
```bash
mv .env.example .env
vi .env
```

Поля в .env
```bash
VK_APP_ID=          # APP ID приложения вк
VK_APP_SECRET=      # Secure key приложения вк
```

Данные для приложения получения можно получить в [настройках своего приложения](https://vk.com/apps?act=manage)


## Запуск
```bash
python main.py
```
Backend доступен на `localhost:8000`
