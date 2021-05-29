# клавиатуры для чат-бота
# главная клавиатура - Правила, Как задать свой вопрос?, Получить ответ
keyboard1 = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Правила"
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Как задать свой вопрос?"
                },
                "color": "positive"
            }
        ]
    ]
}
# клавиатуры блока ответа
# клавиша Сохранить предсказание
keyboard2 = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Сохранить предсказание"
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Задать новый вопрос"
                },
                "color": "secondary"
            }
        ]
    ]
}
# клавиша Скачать файл с предсказанием
keyboard3 = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Скачать файл с предсказанием"
                },
                "color": "primary"
            }
        ]
    ]
}
# клавиша Получить ответ
keyboard4 = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Получить ответ"
                },
                "color": "primary"
            }
        ]
    ]
}
# клавиши Монеты, Бросить монеты
keyboard5 = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Монеты"
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Бросить монеты"
                },
                "color": "positive"
            }
        ]
    ]
}
# клавиша Бросить монеты
keyboard6 = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Бросить монеты"
                },
                "color": "primary"
            }
        ]
    ]
}
keyboard = [keyboard1, keyboard2, keyboard3, keyboard4, keyboard5, keyboard6]
