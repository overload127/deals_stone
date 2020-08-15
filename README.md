# deals_stone
Загрузка сделок клиентов из cvs и выдача 5 самых лучших

Инструкция по установке

Для примера, данный пакет развертывается на ubuntu v20
Установку докера на другие ОС и дистрибутивы можно найти в интернете
Сначала будут выполнены команды по установке докера в ОС
После будут команды для развертывания приложения в докере

============================== 1 ==============================

Открываем терминал (консоль) на хосте и вводим следующие команды (На все вопросы отвечаем - 'y'):


```sudo apt update```
```sudo apt upgrade```

```sudo apt install apt-transport-https ca-certificates curl software-properties-common```
```curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -```
```sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"```
```sudo apt update```
```sudo apt install docker-ce```
```sudo apt  install docker-compose```
```docker-compose --version```

============================== 2 ==============================

Теперь разворачиваем образ и контейнер в докере


```mkdir python_project_1```
```cd python_project_1/'

```sudo apt install git```
```git clone https://github.com/overload127/deals_stone.git```

```cd deals_stone/```

```echo gunicorn == 20.0.4 >> requirements.txt```

Перед запуском, нужно изменить несколько параметров
1) парметр SECRET_KEY и DEBUG в файле deals_stone/settings.py
```
SECRET_KEY = 'YOUR SECRET KEY'
DEBUG = False
```

2) в файле Dockerfile в последней строке ЛОГИН, ПОЧТУ и ПАРОЛЬ суперпользователя

```sudo docker-compose up```


============================== 3 ==============================

Для удаления контейнера и образов:


Вводим команду и находим id всех контейнеров ссылающихся на образ deals_stone_web
```sudo docker ps -a```

Далее удаляем контейнеры
```sudo docker rm <CONTAINER ID>```

Удаляем сам образ
```sudo docker rmi deals_stone_web```