# pyphrasy - Склонение по падежам русских словосочетаний.

Форк реализации [pyphrasy](https://github.com/summerisgone/pyphrasy) с добавлением формата вывода XML, переписан на FastApi

Вся работа основана на библиотеке [pymorpy2](https://pymorphy2.readthedocs.org), которая, в свою очередь,
активно использует словари [OpenCorpora](http://opencorpora.org/).


# Веб-сервис


API
Ожидает запрос с двумя (+1 опциональынй) параметрами:

* phrase - что склонять
* forms - один элемент или список падежей или/и чисел по сокращениям в pymorphy2, разделённые запятой
* response_type - формат результата json | xml (по умолчанию json)

Например: http://example.com/inflect?phrase=склонятор%20словосочетаний&forms=gent,plur&forms=datv&response_type=xml


# Как запустить на своем хостинге

Веб-сервис написан на python и испольузет фреймворк [FastApi](https://github.com/tiangolo/fastapi). Для работы потребуется установка пакетов, указаных в requirements.txt.

По желанию можно использовать [virtualenv](http://www.unix-lab.org/posts/virtualenv/).

Инструкция:

1. Скопировать исходный код с github

1.1. Создать и активировать окружение virtualenv (необязательно)

    $ virtualenv .env
    $ source .env/bin/activate

1.2. Установить зависимости

    $ pip install -r requirements.txt

1.3. Запустить сервис через:
 
1.3.1 Uvicorn

    $ uvicorn main:app --reload
    
1.3.2 Выполнение main.py
        
    $ python3 main.py

2. Проверить работоспособность

    $ curl "http://example.com/inflect?phrase=%D1%80%D0%B0%D0%B1%D0%BE%D1%87%D0%B0%D1%8F%20%D0%BA%D0%BE%D0%BF%D0%B8%D1%8F&cases=accs&cases=datv"
