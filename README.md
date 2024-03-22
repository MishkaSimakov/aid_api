# Сервер для проекта AID

## API

Данные можно получать по двум адресам:

1. `/`: метод POST, принимает на вход JSON в формате:
    ```json
   {
    "category": "profitability"   
   }
    ```
   Возвращает JSON в формате:
    ```json
    {
        "items": {
            "AFKS": {
                "value": -0.013487003433055533
            },
            "AFLT": {
                "value": -0.010980966325036534
            },
            "AGRO": {
                "value": -0.003947553926406222
            }
        },
        "updated_at": "2024-03-22 14:33:40",
        "postfix": "%",
        "message": "success"
    }
    ```
   В `message` содержится `success`, если всё хорошо, и сообщение об
   ошибке, если что-то плохо. Также если что-то плохо,
   то код возврата не 200, а 400.

   В `items` ключами являются компании для отображения на главной странице,
   `value` - показатель этой компании по категории, что передана в запросе.
2. `/tickers/<ticker>/chart`: метод POST, принимает на вход JSON в формате:
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
3. `/tickers/<ticker>/values`: метод POST, ничего не принимает на вход.
   Возвращает JSON в формате:
    ```json
    {
      "ticker_full_name": "Сбербанк России ПАО ао",
      "items": {
        "profitability": {
            "value": 0.0017590149516271136,
            "postfix": "%",
            "should_buy": false,
            "description": "Доходность за период"
        },
        "dividends": {
            "value": 25,
            "postfix": "₽",
            "should_buy": false,
            "description": "Дивиденды за год"
        },
        "relative_dividends": {
            "value": 0.12323770087745242,
            "postfix": "%",
            "should_buy": false,
            "description": "Дивидендная доходность за год"
        }
      },
      "message": "success"
    }
    ```
   