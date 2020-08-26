# Image-resize

Cервис, на основе фреймворка Django, который позволит загружать изображения с компьютера пользователя, или по ссылке, а затем изменять их размер.

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
