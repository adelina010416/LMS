# Бэкенд-часть веб-приложения "LMS"
## Learning Management System

### Запуск приложения
Запуск производится с помощью Docker:

- Собираем образы ```docker-compose build``` 
- Запускаем контейнеры ```docker-compose up```

### Используемые технологии:

- DjangoRestFramework<br>
- Swagger/ReDoc ```host://swagger/```, работает авторизация по Bearer токену<br>
- Redis<br>
- Celery<br>
- Платёжная система Stripe, реализация через сессии<br>
- Пагинация для вывода списка курсов
- DjangoFilters для фильтрации списка платежей