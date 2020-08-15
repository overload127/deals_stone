# deals_stone
Загрузка сделок клиентов из cvs и выдача 5 самых лучших

Инструкция по установке

Для примера, данный пакет развертывается на ubuntu v20
Установку докера на другие ОС и дистрибутивы можно найти в интернете
Сначала будут выполнены команды по установке докера в ОС
После будут команды для развертывания приложения в докере

========= 1 =========

Открываем терминал (консоль) на хосте и вводим следующие команды (На все вопросы отвечаем - 'y'):


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

Теперь разворачиваем образ и контейнер в докере


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

Перед запуском, нужно изменить несколько параметров
1) парметр SECRET_KEY и DEBUG в файле deals_stone/settings.py
```
SECRET_KEY = 'YOUR SECRET KEY'
DEBUG = False
```

2) в файле Dockerfile в последней строке ЛОГИН, ПОЧТУ и ПАРОЛЬ суперпользователя

# Запуск

```
sudo docker-compose up
```


========= 3 =========

Для удаления контейнера и образов:


Вводим команду и находим id всех контейнеров ссылающихся на образ deals_stone_web
```
sudo docker ps -a
```

Далее удаляем контейнеры
```
sudo docker rm <CONTAINER ID>
```

Удаляем сам образ
```
sudo docker rmi deals_stone_web
```

# Процесс работы с сервисом

Отправить свои данные в файле *.csv по адресу в POST запросе:
http://<IP>:<PORT>/api/v1/api_deal/deals/import/csv/

где:
  IP - установленный Вами IP в docker-compose.yml
  PORT Установленный Вами PORT в docker-compose.yml

Варианты ответа:
  Status: OK - файл был обработан без ошибок;
  Status: Error, Desc: <Описание ошибки> - в процессе обработки файла произошла ошибка.


Получить результат по адресу в GET запросе:
http://192.168.1.163:8000/api/v1/api_deal/deals/top/5/

где:
  IP - установленный Вами IP в docker-compose.yml
  PORT Установленный Вами PORT в docker-compose.yml

Варианты ответа:
  "response": [] - значит нет ни одного клиента и сделок
  "response": [...] - набор рассчитаных данных
