# Задание 4. Извлечение данных из Google Sheets

Приложение обновляет Google Spreadsheet таблицу/

Используется библиотеки предоставляемые Google и небольшая [обертка](https://github.com/andy-takker/google-api-service-helper) над их библиотеками. Минимальная версия языка для запуска `3.8+`



## Pre-requisits

Вы должны сделать копию [таблицы](https://docs.google.com/spreadsheets/d/1cmo9ID2VBHHcR1PuzfpZ6yryswyt5YQSubI2ZmRZBqc/edit#gid=0) и указать ID копии, чтобы изменения применились корректно.

## Environments

Перед запуском необходимо указать следующие переменные окружения:

```bash
GOOGLE_SPREADSHEET_ID=  # ID таблицы, которую нужно обновить 
```

И сохранить локально ключи для сервисного аккаунта Google API в файл `./credentials.json`.

## Установка зависимостей

Перед запуском необходимо установить библиотечные зависимости из файла `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```
