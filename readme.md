Документация
------------
VK_bot_izsin - приложение для развлечения и отдыха, которое делает предсказания согласно древнему канону - китайской Книге Перемен.

Настройка программы
-------------------

Необходимые для работы приложения модули перечислены в файле requirements.txt Установка модулей из файла requirements.txt по команде в терминале: \$ pip install -r requirements.txt

Установка программы
-------------------

Достаточно в файл .env ввести данные Вашего сообщества - токен и ID. Бот начнет работать в Вашем сообществе.
Для удобства файл .env предоставляется в готовом виде. Нужно его открыть и ввести свои данные.

Запуск программы
----------------

Запустить приложение из файла VK_bot_izsin/main.py, предварительно заполнив своими данными шаблон файла .env

Инструкция
----------
Управление - после первого запуска появляются кнопки клавиатуры, а также сообщаются ключевые слова, на которые отвечает бот.

Правила простые - ввод команд (ключевых слов) с клавиатуры или нажатие на кнопки, дублирующие эти же команды. 

Слова "Правила" или "правила", или кнопка "Правила" (предусмотрен дубль на английском языке) - вызывает сообщение от бота с правилами сообщества.

Слова "Вопрос" или "вопрос" или кнопка "Как задать вопрос?" (предусмотрен дубль на английском языке) - вызывает сообщение с инструкцией по формулировке вопроса.

Слова "Ответ" или "ответ", или кнопка "Ответ" (предусмотрен дубль на английском языке) - вызывают выдачу предсказания - все толкования взяты из книги Л.В. Нагайцевой "И-Цзин для начинающих".

Слова "Сохранить" или "сохранить", или кнопка "Сохранить предсказание" (предусмотрен дубль на английском языке) - сохраняют предсказание в файл.

Слова "Скачать" или "скачать", или кнопка "Скачать файл с предсказанием" (предусмотрен дубль на английском языке) - вызывают сообщение с прикрепленным файлом предсказания.

Слова "Бросить" или "бросить" или кнопка "Бросить монеты" (предусмотрен дубль на английском языке) - вызывают картинку из 6 монет, упавших случайным образом.

Все остальные слова вызывают возврат к инструкции, как следует задавать вопрос.

Цель гадания - получить ответ на свой вопрос. Полученный ответ можно сохранить в виде текстового файла prognoz.txt, если нажать кнопку "Сохранить предсказаниние" или набрать слова "Сохранить", или "сохранить". Также ответ можно скачать, если набрать слова "Скачать", "скачать" или нажать на кнопку "Скачать файл с предсказанием".

Дополнения
----------
Исходный код хранится на github. Сделаны коммиты по каждой доработке.


Использованные технологии
-------------------------
Работа с чтением и записью текстовых файлов

Работа с БД с использованием подключения к БД SQLite (SQLite3)

Работа с JSON-файлами с использованием библиотеке JSON

Работа с VK_API

Работа с .env файлом через библиотеку OS

Работа с модулем - отдельный файл для хранения пользовательских клавиатур
