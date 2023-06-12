# Foodgram

[![foodgram-app workflow](https://github.com/lazarenkov-e/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/lazarenkov-e/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

Приложение «Продуктовый помощник»: сайт, на котором пользователи могут опубликовать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Server IP:  
[158.160.19.199](http://158.160.19.199/)

### Инструменты:
![image](https://img.shields.io/badge/Python%203.9-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django%204.2-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
### Как запустить проект на боевом сервере:

Установить на сервере docker и docker-compose. Скопировать на сервер файлы docker-compose.yaml и nginx.conf:

```
scp docker-compose.yml <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/docker-compose.yml
scp nginx.conf <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/nginx.conf

```

Добавить в Secrets на Github следующие данные:

```
SECRET_KEY='ваш ключ от Django'
ALLOWED_HOSTS='<адрес вашего сервера>, 127.0.0.1, localhost'
DB_ENGINE=django.db.backends.postgresql # указать, что проект работает с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса БД (контейнера) 
DB_PORT=5432 # порт для подключения к БД
DOCKER_PASSWORD= # Пароль от аккаунта на DockerHub
DOCKER_USERNAME= # Username в аккаунте на DockerHub
HOST= # IP удалённого сервера
USER= # Логин на удалённом сервере
SSH_KEY= # SSH-key компьютера, с которого будет происходить подключение к удалённому серверу
PASSPHRASE= #Если для ssh используется фраза-пароль
TELEGRAM_TO= #ID пользователя в Telegram
TELEGRAM_TOKEN= #ID бота в Telegram

```

Выполнить команды:

*   git add .
*   git commit -m "Коммит"
*   git push

После этого будут запущены процессы workflow:

*   проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest
*   сборка и доставка докер-образа для контейнера web на Docker Hub
*   автоматический деплой проекта на боевой сервер
*   отправка уведомления в Telegram о том, что процесс деплоя успешно завершился

После успешного завершения процессов workflow на боевом сервере должны будут выполнены следующие команды:

```
sudo docker-compose exec web python manage.py migrate

```


```
sudo docker-compose exec web python manage.py collectstatic --no-input 
```

Затем необходимо будет создать суперюзера и загрузить в базу данных информацию об ингредиентах:

```
sudo docker-compose exec web python manage.py createsuperuser

```

```
sudo docker-compose exec web python manage.py load_data_csv --path <путь_к_файлу> --model_name <имя_модели> --app_name <название_приложения>

```
### Автор проекта

**Лазаренков Евгений** 