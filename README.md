# Events manager SPA (Django, DRF, PostgreSQL, Vue.js)
#### Описание:
- Full stack приложение для управления событиями (CRUD операции).
- Бэкенд работает на Django, Django Rest Framework и PostgreSQL
- Фронтенд работает на Vue.js
- Адрес приложения локально: http://127.0.0.1:8080/
- Требуется авторизация существующего пользователя по логину и паролю.
- Пользователей заранее создает администратор проекта.
- При успешной авторизации система выдает существующие события текущего пользователя и активирует кнопки фильтра и операций с событиями.
- Доступны фильтрация событий по дате старта (выпадающий список) и по части наименования.
- Применена пагинация  
- Применяется органичение по кол-ву запросов с фронта к API в день для пользователя (throttling).  
- По адресу http://127.0.0.1:8000/api/alert/ система выбирает все события, начинающиеся в течение часа от текущего момента, и при наличии заполненного адреса эл. почты в профиле автора события отправляет ему напоминание.
- Необходимо поставить на cron скрипт, ходящий командой `curl` или `wget` на указанный урл для отправки напоминаний автоматически по расписанию (например, раз в час).

#### Для запуска приложения локально требуется:
- На бэкенде:
   - в вирт. окружении установить требуемые зависимости из requirements.txt
   - указать настройки подключения к БД и к эл. адресу для отправки напоминаний,
   - создать суперпользователя 
   - выполнить миграции
   - создать пользователей системы
   - запустить дев сервер django.

- На фронтенде:
   - установить Node.js
   - установить vue
   - установить vue cli
   - запустить дев сервер vue
   
 #### Скриншот фронт: https://www.screencast.com/t/i3xKgVR5AB4
 #### Скриншот полученного email-напоминания: https://www.screencast.com/t/oIah7rHM5Owm
