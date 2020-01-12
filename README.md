# Test-task-ITIS
Log-files analysis

Чтобы запустить приложение:
> python3 web.py   

В браузере:
localhost:5000/site

my_log_parser -- разбирает лог файл и заполняет БД.

get_answers -- модуль с запросами к БД, соответствующим вопросам.

web.py -- локальный сервер на flask, отправляющий пользователю ответы на 
post-запросы в виде html шаблонов, находящихся по адресу: /templates/ans{1,2,3}.html 
