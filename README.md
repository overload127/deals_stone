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

Создаем файл виртуальных переменных окружения продакшена:
```
nano .env.prod
```

Скопируйте и замените на свои параметры следующие строки:
```
DJANGO_DEBUG=0
DGANGO_SECRET_KEY=<Ваш секретный ключ/любая строка>
DJANGO_ALLOWED_HOSTS=<ip адреса через пробел. '*' - любой адрес>
DJANGO_IP_PORT=8000
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=<Название БД в системе управления БД>
SQL_USER=<Логин админа для БД>
SQL_PASSWORD=<Пароль админа для БД>
SQL_HOST=db
SQL_PORT=<порт для БД>

POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

2) в файле Dockerfile (находится в папке deals_stone) в последней строке нужно сменить ЛОГИН, ПОЧТУ и ПАРОЛЬ суперпользователя web-приложения

========= 3 =========
# Запуск

```
sudo docker-compose up
```


========= 4 =========
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

========= 5 =========
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

