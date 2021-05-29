import json
import random
import sqlite3
from os import environ as env

import vk_api
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import keyboards


def work_in_db(n):
    """
    функция, которая обслуживает работу с БД по поиску предсказания
    n - выпавшее при гадании случайное число из отрезка [0, 63]
    :return: подключение и создание курсора в имеющейся БД и выдача прогноза в виде сообщения
    """
    con = sqlite3.connect("db/izsin.db")
    cur = con.cursor()
    result = cur.execute("""SELECT name, rus_name, unicode FROM hexx
                    WHERE ID = ?""", (n,)).fetchone()
    pr = open(f'data/Prognoz/{result[1]}.txt').encode('cp-1251').decode('utf-8').read()
    con.close()
    print(result)
    return result, pr


def main():
    """
    работа чат-бота по запросам от пользователя
    :return: сообщения чат-бота с прогнозом из БД по случайному числу, выданное в личном чате сообщества, или ответы на запросы
    """
    load_dotenv()  # .env
    vk_session = vk_api.VkApi(token=env['VK_TOKEN'])  # токен
    longpoll = VkBotLongPoll(vk_session, int(env['VK_BOT_ID']))  # ID
    vk = vk_session.get_api()  # открытие сессии
    m = -1  # параметр для отслеживания выдачи ответов без бросания монет
    # запуск сессии чат-бота
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            from_id = event.obj.message['from_id']
            text = event.obj.message['text'].lower()
            print(f'Новое сообщение {text} от {from_id}')  # оповещение о новом сообщении от пользователя
            # обработка сообщений пользователя
            # запрос на получение ответа
            if text in ['получить ответ', 'ответ', 'answer']:
                if m == -1:
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=json.dumps(keyboards.keyboard[5], ensure_ascii=False),
                        message=f'Вы хотите получить ответ без бросания монет? Так ничего не получится. Нужно строго соблюдать ритуал! \n \n'
                                f'Пожалуйста, наберите "Бросить" или "бросить" или нажмите на кнопку "Бросить монеты"',
                        random_id=random.randint(0, 2 ** 64)
                    )
                else:
                    # получение по числу m предсказания из БД
                    mess = work_in_db(m)
                    # печать картинки гексаграммы из БД
                    attachments = []
                    from vk_api import VkUpload
                    upload = VkUpload(vk_session)
                    image = f'data/Img/{m}.png'
                    photo = upload.photo_messages(photos=image)[0]
                    attachments.append(
                        'photo{}_{}'.format(photo['owner_id'], photo['id'])
                    )
                    vk.messages.send(
                        user_id=from_id,
                        attachment=','.join(attachments),
                        random_id=random.randint(0, 2 ** 64)
                    )
                    # печать текста предсказания и выдача клавиатуры для дальнейших действий
                    vk.messages.send(
                        user_id=from_id,
                        keyboard=json.dumps(keyboards.keyboard[1], ensure_ascii=False),
                        message=f'Вам выпала гексаграмма {chr(mess[0][2])} {mess[0][0]} - {mess[0][1]} \n \n Ее значение: \n {mess[1]} \n \n'
                                f'Если Вы хотите сохранить предсказание, то напишите "сохранить" или "Сохранить", или нажмите '
                                f'кнопку "Сохранить предсказание"',
                        random_id=random.randint(0, 2 ** 64)
                    )
                    m = -1
            # запрос на сохранение ответа
            elif text in ['сохранить предсказание', 'сохранить', 'save']:
                f = open('prognoz.txt', 'w')
                st = ''.join(f'Вам выпала гексаграмма {mess[0][0]} - {mess[0][1]} \n \n Ее значение: \n {mess[1]}')
                f.write(st)
                f.close()
                # информация для пользователя о сохранении предсказания и выдача клавиатуры для дальнейших действий
                vk.messages.send(
                    user_id=from_id,
                    keyboard=json.dumps(keyboards.keyboard[2], ensure_ascii=False),
                    message=f'Предсказание сохранено. \n \n'
                            f'Если Вы хотите скачать сохраненное предсказание, то напишите "Скачать" или "скачать", или '
                            f'нажмите кнопку "Скачать файл с предсказанием"',
                    random_id=random.randint(0, 2 ** 64)
                )
            # запрос на скачивание файла с ответом
            elif text in ['скачать файл с предсказанием', 'скачать', 'download']:
                attachments = []
                from vk_api import VkUpload
                upload = VkUpload(vk_session)
                pr = f'data/Prognoz/{mess[0][1]}.txt'
                document = upload.document_message(doc=pr, title='Ваше предсказание', peer_id=from_id)
                print(document)
                attachments.append(
                    'doc{}_{}'.format(document['doc']['owner_id'], document['doc']['id'])
                )
                # выдача файла с предсказанием пользователю
                vk.messages.send(
                    keyboard=json.dumps(keyboards.keyboard[0], ensure_ascii=False),
                    user_id=from_id,
                    attachment=','.join(attachments),
                    random_id=random.randint(0, 2 ** 64)
                )
            # запрос, как задать вопрос или для задания нового вопроса
            elif text in ['вопрос', 'как задать свой вопрос?', 'задать новый вопрос', 'question']:
                # описание действия при формулировке вопроса и выдача клавиатуры для дальнейших действий
                vk.messages.send(
                    user_id=from_id,
                    keyboard=json.dumps(keyboards.keyboard[4], ensure_ascii=False),
                    message=f'В гадании принято бросать шесть монет для формирования гексаграммы ответа. \n \n'
                            f'Монеты падают случайным образом, каждая из них будет лежать одной стороной вверх -'
                            f' орлом или решкой, это и сформирует нужный для предсказания код. \n \n'
                            f'Если Вы первый раз зашли на ресурс и не знакомы с монетами И-Цзин, нажав на кнопку '
                            f'"Монеты", Вы получите информацию о сторонах монеты И-Цзин. \n \n'
                            f'Хорошо продумайте свой вопрос, задайте его Высшим силам и нажмите кнопку "Бросить монеты".',
                    random_id=random.randint(0, 2 ** 64)
                )
            # запрос на бросание монет
            elif text in ['бросить монеты', 'бросить', 'toss coins']:
                # получение случайного числа от 0 до 63
                m = random.randint(0, 63)
                # формирование его двоичного кода
                mm = bin(m)[2:]
                # дополнение двоичного кода до 6 знаков не значащими нулями
                if len(mm) < 6:
                    mm = (6 - len(mm)) * '0' + mm
                # разбор кода и составление набора из 6 монет - орлы и решки
                attachments = []
                for x in mm:
                    if x == '0':
                        from vk_api import VkUpload
                        upload = VkUpload(vk_session)
                        image = f'data/Img/moneta_reshka.png'
                        photo = upload.photo_messages(photos=image)[0]
                        attachments.append(
                            'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        )
                    else:
                        from vk_api import VkUpload
                        upload = VkUpload(vk_session)
                        image = f'data/Img/moneta_orel.png'
                        photo = upload.photo_messages(photos=image)[0]
                        attachments.append(
                            'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        )
                # печать картинки конфигурации монет
                vk.messages.send(
                    user_id=from_id,
                    attachment=','.join(attachments),
                    random_id=random.randint(0, 2 ** 64)
                )
                # пояснения к расшифровке картинки и выдача клавиатуры для дальнейших действий
                vk.messages.send(
                    user_id=from_id,
                    keyboard=json.dumps(keyboards.keyboard[3], ensure_ascii=False),
                    message=f'Гексаграмма записывается снизу вверх, т.е. первая монета определяет нижнюю черту и так далее. \n'
                            f'Сплошная линия соответствует орлу, прерванная линия - решке. \n \n'
                            f'Нажмите кнопку "Получить ответ" или наберите текст "ответ" или "Ответ". \n \n'
                            f'Вы получите предсказание по Вашему вопросу согласно комбинации выпавших монет.',
                    random_id=random.randint(0, 2 ** 64)
                )
            # запрос на получение команд бота
            elif text in ['правила', 'rules', 'commands']:
                # правила общения в сообществе
                vk.messages.send(
                    user_id=from_id,
                    keyboard=json.dumps(keyboards.keyboard[0], ensure_ascii=False),
                    message=f'Правила для управления ботом: \n \n'
                            f'Для демонстрации клавиатуры нужно набрать сообщение с текстом "Клавиатура" или "клавиатура".\n \n'
                            f'Для повторного ознакомления с правилами наберите "правила" или "Правила", или нажмите кнопку "Правила" \n \n'
                            f'Для того, чтобы получить указания, что делать дальше, наберите "вопрос" или "Вопрос", или '
                            f'нажмите кнопку "Как задать свой вопрос?"\n \n'
                            f'Далее - следуйте инструкциям бота.\n \n'
                            f'Удачи Вам и исполнения желаний!',
                    random_id=random.randint(0, 2 ** 64)
                )
            # запрос на получение стартовой клавиатуры - кнопок бота
            elif text in ['клавиатура', 'keyboard']:
                # настройка стартовой клавиатуры для пользователя
                vk.messages.send(
                    user_id=from_id,
                    keyboard=json.dumps(keyboards.keyboard[0], ensure_ascii=False),
                    key=(env['VK_TOKEN']),
                    random_id=random.randint(0, 2 ** 64),
                    message='Держи!'
                )
            # запрос на получение информации о монетах И-Цзин
            elif text in ['coins', 'монеты', 'coin', 'монета']:
                # информация об орле и решке монет И-Цзин
                from vk_api import VkUpload
                upload = VkUpload(vk_session)
                image = f'data/Img/moneta_orel.png'
                photo = upload.photo_messages(photos=image)[0]
                attachments = []
                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
                vk.messages.send(
                    user_id=from_id,
                    attachment=','.join(attachments),
                    message=f'Лицевая сторона монеты - орел',
                    random_id=random.randint(0, 2 ** 64)
                )
                attachments = []
                image = f'data/Img/moneta_reshka.png'
                photo = upload.photo_messages(photos=image)[0]
                attachments.append(
                    'photo{}_{}'.format(photo['owner_id'], photo['id'])
                )
                vk.messages.send(
                    user_id=from_id,
                    keyboard=json.dumps(keyboards.keyboard[5], ensure_ascii=False),
                    attachment=','.join(attachments),
                    message=f'Тыльная сторона монеты - решка.',
                    random_id=random.randint(0, 2 ** 64)
                )
                vk.messages.send(
                    user_id=from_id,
                    keyboard=json.dumps(keyboards.keyboard[5], ensure_ascii=False),
                    message=f'Хорошо продумайте свой вопрос, задайте его Высшим силам и нажмите кнопку "Бросить монеты".',
                    random_id=random.randint(0, 2 ** 64)
                )
            # вступительный текст с инструкцией для нерегламентированных сообщений от пользователя
            else:
                vk.messages.send(
                    user_id=from_id,
                    keyboard=json.dumps(keyboards.keyboard[0], ensure_ascii=False),
                    key=(env['VK_TOKEN']),
                    message=f'Если Вы в первый раз пользуетесь нашим ресурсом, то нужно ознакомиться с Правилами сообщества. \n \n'
                            f'Для этого введите "правила" или "Правила" в строку сообщения, или нажмите кнопку "Правила" \n \n'
                            f'Для тех, кто уже знаком с правилами, - введите "вопрос" или "Вопрос", или нажмите кнопку "Как задать свой вопрос?',
                    random_id=random.randint(0, 2 ** 64)
                )
        # обработка событий, когда долго нет пользователей - для сохранения онлайн сессии от прерываний со стороны ВК
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            event_id = event.obj.message['event_id']
            vk.messages.send(
                user_id=from_id,
                event_id=event_id,
                keyboard=json.dumps(keyboards.keyboard[0], ensure_ascii=False),
                message=f'Жду вопросов...',
                random_id=random.randint(0, 2 ** 64)
            )


if __name__ == '__main__':
    main()
