#### Скрипт для обновления остатков товаров из МойСклад в Insales
###### Особенности работы
Товар в МС без модификаций, то есть каждая модификация товара представляет собой
отдельный товар.
Товар в Insales — с модификациями (то есть, один общий товар с вариантами).
Стандартная синхронизация не позволяет связывать такие товары.
Новые товары создаются вручную в обеих системах. Если у них совпадают артикулы, то остатки
синхронизируются. Товаров около 1000. Обновление раз в час. Это позволяет обойтись без применения асинхронных запросов (полное обновление занимает менее 1,5 минут).

###### Алгоритм работы
1. Получаем из МойСклад все товары, для которых задан артикул. Он будет являться ключом для сопоставления товаров в обеих системах.
2. Получаем из InSales полный список вариантов товаров.
3. Находим все совпаения артикулов и формируем список вариантов для обновления.
4. Обновляем остатки в InSales (API допускает обновление не более 100 вариантов за 1 запрос).

###### Инструкция по установке
1. Поместите файлы скрипта в отдельную папку, например /home/user/script. ВАЖНО:
  * Не помещайте файлы в общедоступные папки, например, директории веб-сервера, это небезопасно.
  * Не удаляйте папку temp (изначально пустую), она нужна для сохранения лога и файлов для отладки.

2. Python3 должен быть установлен на сервере:
```bash
user@sever:$ which python3
/usr/local/bin/python3
```
Точная версия не важна: скрипт должен работать с любой версией интерпретатора Python 3.x

3. Создайте виртуальную среду:
```bash
user@sever:$ python3 -m venv /path/to/environment
```
Проще всего разместить её в самой папке со скриптом. Для этого замените /path/to/ на полный путь к папке.

4. Активируйте виртуальную среду:
```bash
user@sever:$ source /path/to/environment/bin/activate
(environment) user@sever:$
```

5. Установите менеджер пакетов pip, если он не установлен:
```bash
(environment) user@sever:$ python3 -m ensurepip --default-pip
```

6. Скрипт требует для работы единственного дополнительного пакета requests. Установите его:
```bash
(environment) user@sever:$ pip install requests
```

7. Создайте (измените) shell-скрипт для удобного запуска скрипта по расписанию:
```run_script.sh
#!/bin/bash
cd /path/to/script
source environment/bin/activate
python3 main.py
```

8. Добавьте в crontab строку для запуска скрипта каждый час:
```crontab
* 0-23 * * * /path/to/script/run_script.sh
```

9. Для того, чтобы переключиться на другой аккаунт МойСклад:
  * создайте API-ключ (токен) в новом аккаунте (https://online.moysklad.ru/app/#token)
  * замените значение MOYSKLAD_TOKEN в файле setup.py новым ключом (файл setup.py можно открыть в любом текстовом редакторе).
