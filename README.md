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
       "tickers": {
           "AFKS": {
               "value": -0.017018146150073576
           },
           "AFLT": {
               "value": -0.017569546120058566
           },
           "AGRO": {
               "value": -0.005357394614408539
           }
       },
        "indices": {
            "MOEX10": {
                "name": "Индекс Мосбиржи",
                "tickers": {
                    "SBER": 12,
                    "OZON": 38,
                    "VKCO": 16
                }
            },
            "MOEXRE": {
                "name": "Ещё какой-то индекс",
                "tickers": {
                    "SBER": 31,
                    "OZON": 12,
                    "VKCO": 32
                }
            }
        },
       "updated_at": "2024-03-22 16:17:31",
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
      "period": "H"   
   }
   ```
   Возвращает JSON в формате:
   ```json
   {
   "items": [
        {
            "open": 296.12,
            "close": 296.16,
            "high": 296.17,
            "low": 296.1,
            "begin": "2024-03-22 15:24:00",
            "end": "2024-03-22 15:24:59"
        },
        {
            "open": 296.25,
            "close": 296.29,
            "high": 296.3,
            "low": 296.24,
            "begin": "2024-03-22 15:26:00",
            "end": "2024-03-22 15:26:59"
        }
    ],
    "message": "success"
   }
   ```
3. `/tickers/<ticker>/values`: метод POST, ничего не принимает на вход.
   Возвращает JSON в формате:
    ```json
    {
      "short_name": "Сбербанк",
      "full_name": "Сбербанк России ПАО ао",
      "price": 123123.123,
      "items": {
        "profitability": {
            "value": 1.7590149516271136,
            "postfix": "%",
            "verdict": 1,
            "name": "Доходность за период",
            "description": "Это очень интересная величина, она считается так-то так-то..."
        }
      },
      "message": "success"
    }
    ```
4. `/categories`: метод POST, ничего не принимает на вход.
   Возвращает JSON в формате:
   ```json
   {
	  "categories": [
		  "profitability",
		  "dividends",
		  "relative_dividends",
	   	  "atr"
	  ],
	  "message": "success"
   }
   ```
5. `/images/<ticker>.png`: метод GET.
   Возвращает картинку для данного тикера в формате png. Не для всех тикеров есть картинки!
