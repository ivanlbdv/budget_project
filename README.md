# Бюджет‑трекер
## Описание проекта
Бюджет‑трекер - веб‑приложение для учёта личных финансов, позволяющее пользователям:

- Фиксировать доходы и расходы;
- Анализировать траты по категориям и периодам;
- Визуализировать данные через интерактивные графики;
- Экспортировать историю операций в CSV.

## Используемые технологии
- Python 3.10.11
- Django 3.2.16
- PostgreSQL
- Bootstrap 5 (адаптивный интерфейс)
- Chart.js (построение графиков)
- Django ORM (работа с базой данных)

## Локальный запуск проекта
- Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone git@github.com:ivanlbdv/budget_project.git
cd budget_project
```
- Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/Scripts/activate
```
- Обновите пакетный менеджер:

```bash
python -m pip install --upgrade pip
```
- Установите модули из файла requirementst.txt:

```bash
pip install -r requirements.txt
```

- Создайте файл .env и добавьте в него:

```   
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=budget_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

- Выполните миграции:

```bash
python manage.py migrate
```

- Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

Следуйте инструкциям в терминале для ввода email и пароля.

- Запустите сервер разработки:

```bash
python manage.py runserver
```

Проект будет доступен по адресу: http://127.0.0.1:8000/

## Автор:
Иван Лебедев
https://github.com/ivanlbdv
