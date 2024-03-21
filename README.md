# Сервер для проекта AID

## API
Данные можно получать по двум адресам:
1. `/`: метод POST, принимает на вход JSON в формате:
    ```json
   {
    "category": "return"   
   }
    ```
    Возвращает JSON в формате:
    ```json
    {
      "message": "success",
      "items": {
        "SBER": 0.01,
        "ROSN": 0.12,
        "VTB": -0.01
      },
      "postfix": "%"
    }
    ```
    В `message` содержится `success`, если всё хорошо, и сообщение об
    ошибке, если что-то плохо. Также если что-то плохо,
    то код возврата не 200, а 400.
    
    В `items` ключами являются компании для отображения на главной странице, 
    значение по этому ключу - показатель данной компании по той категории,
    что передана в запросе.
2. `/tickers/<ticker>/charts`: метод POST, принимает на вход JSON в формате:
    ```json
   {
    "period": "1Y"   
   }
    ```
    Возвращает JSON в формате:
    ```json
    {
    "message": "success",
    "items": [
        {
            "value": 204.01,
            "begin": "2023-03-27 00:00:00",
            "end": "2023-04-01 00:00:00"
        },
        {
            "value": 218.45,
            "begin": "2023-04-03 00:00:00",
            "end": "2023-04-08 00:00:00"
        },
        {
            "value": 217.1,
            "begin": "2023-04-10 00:00:00",
            "end": "2023-04-15 00:00:00"
        },
        {
            "value": 222.98,
            "begin": "2023-04-17 00:00:00",
            "end": "2023-04-22 00:00:00"
        }
      ]
    }
    ```
   