# Auth System (Django + JWT + RBAC)
## Описание проекта

Проект реализует систему аутентификации и авторизации пользователей с использованием JWT-токенов и модели управления доступом на основе ролей (RBAC).
Основные возможности:

* регистрация и логин пользователей
* JWT-аутентификация
* разграничение прав доступа (RBAC)
* защищённые API endpoints
* мягкое удаление пользователей (soft delete)

**Аутентификация** — процесс проверки личности пользователя.
В проекте реализована через JWT-токен.

**Авторизация** — процесс определения прав доступа пользователя.
Реализована через RBAC (Role-Based Access Control).

## Архитектура системы
User-> UserRole-> Role-> AccessRule-> BusinessElement

Описание:
* **User** — пользователь системы
* **Role** — роль (admin, user и т.д.)
* **UserRole** — связь пользователя и роли
* **BusinessElement** — защищаемый ресурс (например: products)
* **AccessRule** — права доступа (read, write и т.д.)

## Как работает система
1. Пользователь отправляет логин/пароль
2. Система возвращает JWT-токен
3. Токен передается в заголовке:

   ```
   Authorization: Bearer <token>
   ```
4. Middleware извлекает пользователя из токена
5. При запросе:
   * проверяется аутентификация
   * определяется роль пользователя
   * проверяются права доступа через AccessRule

---

## API Endpoints
### Логин

**POST /api/users/login/**
Request:
```json
{
  "email": "admin@test.com",
  "password": "1234"
}
```

Response:
```json
{
  "token": "JWT_TOKEN"
}
```
---

### Получение продуктов
**GET /api/mock/products/**

Headers:
```
Authorization: Bearer <token>
```

---
### Удаление пользователя (Soft Delete)

**DELETE /api/users/delete/**

Headers:
```
Authorization: Bearer <token>
```

Response:
```json
{
  "message": "User deactivated"
}
```

---

## Сценарии работы (обязательно для проверки)
### Без токена
```json
{
  "error": "Unauthorized"
}
```
---

### Нет прав доступа
```json
{
  "error": "Forbidden"
}
```
### Успешный доступ

```json
[
  {"id": 1, "name": "Laptop"},
  {"id": 2, "name": "Phone"}
]
```
---

## Soft Delete
В системе реализовано мягкое удаление пользователей.
При удалении:
* пользователь НЕ удаляется из базы
* поле `is_active` устанавливается в `False`

Преимущества:
* сохранение данных
* сохранение связей
* безопасность

Неактивный пользователь:
* не может залогиниться
* не получает доступ к API

## Реализация безопасности
* JWT используется вместо сессий
* CSRF отключён для API (так как используется stateless аутентификация)
* проверка пользователя происходит через middleware
* доступ контролируется через декораторы
  
## Технологии
* Python 3
* Django
* Django REST Framework
* SQLite
---

## Запуск проекта

```bash
python manage.py migrate
python manage.py runserver
```

---

## Тестирование

Использовался Postman.
Шаги:
1. Выполнить POST /api/users/login/
2. Получить JWT токен
3. Передать токен в Authorization header
4. Сделать запрос к защищенному endpoint

## Особенности реализации

* кастомная модель пользователя
* собственная реализация JWT (без сторонних библиотек)
* middleware для аутентификации
* декораторы для проверки прав
* гибкая RBAC система

---

## Пример настройки прав
```python
role = Role.objects.create(name="admin")
element = BusinessElement.objects.create(name="products")

AccessRule.objects.create(
    role=role,
    element=element,
    read=True
)
```

---

## Заключение

Реализована полноценная система:
* аутентификации (JWT)
* авторизации (RBAC)
* контроля доступа к API

