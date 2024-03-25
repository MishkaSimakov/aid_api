# Сервер для проекта AID

## API

Данные можно получать по двум адресам:

1. `/`: метод GET, принимает на вход JSON в формате:
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
               "value": -0.017018146150073576
           },
           "AFLT": {
               "value": -0.017569546120058566
           },
           "AGRO": {
               "value": -0.005357394614408539
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
2. `/tickers/<ticker>/chart`: метод GET, принимает на вход JSON в формате:
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
3. `/tickers/<ticker>/values`: метод GET, ничего не принимает на вход.
   Возвращает JSON в формате:
    ```json
    {
      "ticker_full_name": "Сбербанк России ПАО ао",
      "price": 123123.123,
      "items": {
        "profitability": {
            "value": 0.0017590149516271136,
            "postfix": "%",
            "verdict": 1,
            "description": "Доходность за период"
        },
        "dividends": {
            "value": 25,
            "postfix": "₽",
            "verdict": 0,
            "description": "Дивиденды за год"
        },
        "relative_dividends": {
            "value": 0.12323770087745242,
            "postfix": "%",
            "verdict": -1,
            "description": "Дивидендная доходность за год"
        }
      },
      "message": "success"
    }
    ```
4. `/categories`: метод GET, ничего не принимает на вход.
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
   
