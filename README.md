# deals_stone
Загрузка сделок клиентов из cvs и выдача 5 самых лучших

Инструкция по установке

Для примера, данный пакет развертывается на ubuntu v20
Установку докера на другие ОС и дистрибутивы можно найти в интернете
Сначала будут выполнены команды по установке докера в ОС
После будут команды для развертывания приложения в докере

========= 1 =========
# Открываем терминал (консоль) на хосте и вводим следующие команды (На все вопросы отвечаем - 'y'):


```
sudo apt update
```
```
sudo apt upgrade
```

```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
```
```
sudo apt update
```
```
sudo apt install docker-ce
```
```
sudo apt  install docker-compose
```
```
docker-compose --version
```

========= 2 =========
# Теперь разворачиваем образ и контейнер в докере


```
mkdir python_project_1
```
```
cd python_project_1/
```

```
sudo apt install git
```
```
git clone https://github.com/overload127/deals_stone.git
```

```
cd deals_stone/
```

```
echo gunicorn == 20.0.4 >> requirements.txt
```

Все настройки находятся в файле docker-compose.yml
Открываем файл:
```
nano docker-compose.yml
```

Описание строк настройки:
```
DJANGO_DEBUG=<включает и отключает режим отладки>
DGANGO_SECRET_KEY=<Ваш секретный ключ/любая строка>
DJANGO_ALLOWED_HOSTS=<ip адреса через пробел. '*' - любой адрес>
DJANGO_IP_PORT=<порт веб приложения>
SQL_ENGINE=<Тип базы данных>
SQL_DATABASE=<Название БД в системе управления БД>
SQL_USER=<Логин админа для БД>
SQL_PASSWORD=<Пароль админа для БД>
SQL_HOST=<ip БД><Лучше всего использовать 'db' - оно указывает на контейнер с БД>
SQL_PORT=<port БД><Просто ставьте внутренний ip контейнера БД '5432'>
```

Второй блок настроек (Находится ниже)
```
POSTGRES_USER=<как в SQL_USER>
POSTGRES_PASSWORD=<как в SQL_PASSWORD>
POSTGRES_DB=<как в SQL_DATABASE>
```

Пример простых настроек (Никогда их не используйте):
```
- DJANGO_DEBUG=0
- DGANGO_SECRET_KEY=my_secret_key_322_3_xya
- DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] *
- DJANGO_IP_PORT=8000
- SQL_ENGINE=django.db.backends.postgresql
- SQL_DATABASE=django_prod
- SQL_USER=admin
- SQL_PASSWORD=admin_pgs
- SQL_HOST=db
- SQL_PORT=5432
```

Второй блок настроек (Находится ниже)
```
- POSTGRES_USER=admin
- POSTGRES_PASSWORD=admin_pgs
- POSTGRES_DB=django_prod
```

========= 3 =========
# Первый запуск

Собираем все 3 контейнера и запускаем 3 образа в фоновом режиме
```
sudo docker-compose -f docker-compose.yml up -d --build
```

Подготавливаем все необходимые миграции и выполняем их
```
sudo docker-compose -f docker-compose.yml exec web python manage.py makemigrations api_deal --noinput
```

```
sudo docker-compose -f docker-compose.yml exec web python manage.py makemigrations --noinput
```

```
sudo docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
```

Собираем все статические файлы
```
sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
```

Создаем суперпользователя
```
sudo docker-compose -f docker-compose.yml exec web python manage.py createsuperuser 
```

Выключаем контейнеры
```
sudo docker-compose -f docker-compose.yml down
```

========= 4 =========
# Запуск

Запуск с выводом на консоль
```
sudo docker-compose up --build
```

Запуск в фоновом режиме
```
sudo docker-compose -f docker-compose.yml up -d --build
```

========= 5 =========
# Остановка
Если контейнеры запущены с выводом на консоль, то просто ctrl+c

Если работают в фоновом режиме, то вводим команду:

```
sudo docker-compose -f docker-compose.yml down
```

========= 6 =========
# Процесс работы с сервисом

Отправить свои данные в файле *.csv по адресу в POST запросе:
http://<_IP>:<_PORT>/api/v1/api_deal/deals/import/csv/

где:
  _IP - установленный Вами IP в docker-compose.yml
  _PORT Установленный Вами PORT в docker-compose.yml

Варианты ответа:
  Status: OK - файл был обработан без ошибок;
  Status: Error, Desc: <Описание ошибки> - в процессе обработки файла произошла ошибка.


Получить результат по адресу в GET запросе:
http://<_IP>:<_PORT>/api/v1/api_deal/deals/top/5/

где:
  _IP - установленный Вами IP в docker-compose.yml
  _PORT Установленный Вами PORT в docker-compose.yml

Варианты ответа:
  "response": [] - значит нет ни одного клиента и сделок
  "response": [...] - набор рассчитаных данных

========= 7 =========
# Для удаления контейнера и образов:


Вводим команду и находим id всех контейнеров ссылающихся на образ deals_stone_web. Так же будут выведены и другие контейнеры. В этом приложениии используются образы "deals_stone_nginx" "postgres:12.0-alpine". На их основании были созданы специальные контейнеры. В случае если вы уверены что у Вас было создано только это приложение, и нет других зависящих программ, то для полного удаления вы можете выполнять приведенные ниже команды ко всем образам и контейнерам из команды (sudo docker ps -a)
```
sudo docker ps -a
```

Далее удаляем контейнеры (Для каждого найденого если уверены что нет других зависимостей)
```
sudo docker rm <CONTAINER ID>
```

Удаляем сам образ (А так же "deals_stone_nginx" "postgres:12.0-alpine" если уверены что на них никто не работает)
```
sudo docker rmi deals_stone_web
```

