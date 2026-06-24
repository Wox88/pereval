# Перевалы API (Pereval API)

Этот проект представляет собой RESTful API, разработанный с использованием Django и Django REST Framework для управления данными о перевалах. Пользователи могут добавлять данные о перевалах, обновлять их и получать информацию по электронной почте.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/ваш_путь_к_репозиторию.git
    cd ваш_каталог_для_проекта
    ```

2. Создайте и активируйте виртуальную среду:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux или Mac
    venv\Scripts\activate  # Для Windows
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Выполните миграции для создания базы данных:
    ```bash
    python manage.py migrate
    ```

5. Запустите сервер:
    ```bash
    python manage.py runserver
    ```

## Использование API

### Добавление перевала

**POST** `/add/`

**Тело запроса:**
```json
{
    "latitude": 43.3521,
    "longitude": 42.4789,
    "height": 2850,
    "name": "Перевал Северный",
    "user_name": "Иван Петров",
    "user_email": "ivan.petrov@example.com",
    "user_phone": "+79991234567",
    "images": []  // Список изображений (отправляйте их отдельно через форму)
}
