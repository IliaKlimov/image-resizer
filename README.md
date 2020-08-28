# Image-resize

Cервис, на основе фреймворка Django, который позволяет загружать изображения с компьютера пользователя или по ссылке, на сервер, а затем изменять их размер.

### Установка
```
pip install -r requirements.txt
```
##### Подготовка базы данных
```
python manage.py migrate --run-syncdb
```
##### Запуск сервера
```
python manage.py runserver
```

### Установка через Docker
Находясь в папке с проектом, выполнить команду
```
$ docker-compose up -d --build
```
