# Сервер и интерфейс для проекта AID

Второй проект по Python.

## Инструкции по запуску

Для запуска приложения есть скрипт `serve.sh`, который сначала собирает фронтенд,
а затем запускает сервер.

## Идея

Сайт, который будет отображать базовую финансовую информацию о компаниях, фигурирующих на Мосбирже.
Интерфейс будет состоять из 2-x основных страниц: главная и страница детальной информации о компании.
На главной странице можно будет увидеть список компаний, отсортировать его по разным показателям.
С главной страницы можно перейти на страницу деталей о компании.
Там можно посмотреть график за разные периоды времени, а также основные финансовые показатели.
Вся информация для интерфейса будет получаться из API, которое будет написано на Python.

## Используемые технологии

На Python основная библиотека - это Flask, также используется несколько математических библиотек
для вычисления различных финансовых показателей.
Со стороны фронтенда будут использоваться HTML + CSS (Bootstrap) + JS (возможно с Vue)

## Архитектура

Общая архитектура приложения такова:
Есть приложение на основе Vue, которое динамически делает запросы к API.
API работает на Python.
Для каждого типа запроса есть отдельный файл в папке app/routes, в котором описаны верхнеуровневые вычисления,
необходимые для ответа на запрос.
Для формирования единого flask-приложения из этих кусков используются Flask Blueprints, которые
позволяют настроить каждый вид запроса в отдельном файле.

За получение и обработку информации с Мосбиржи отвечает класс Ticker из файла app/financial/ticker.py
Абстрактно он представляет из себя информацию об одном тикере.
Основной его источник данных - свечи, хранятся в массиве candles.
Этот массив лениво загружается с сервера при необходимости.
Для этого сделан декоратор @assure_candles_loaded, который перед входом в тело функции проверяет, что
данные загружены.

Для более полезной информации о компании есть индикаторы.
Они представлены классом TickerIndicator в файле app/financial/ticker.py
Индикатор - это какая-то вычисляемая функция от данных о тикере, которая позволяет
сделать какие-то осмысленные (а может и нет) предсказания.
Индикатор содержит в себе название, описание, постфикс (например % или ₽), само значение индикатора,
а также вердикт - стоит ли покупать тикер, основываясь на значении данного индикатора.

Помимо данных об отдельном тикере на главной странице будет отображаться общая информация о рынке.
Для получения всех необходимых данных необходимо сделать множество запросов, поэтому эти запросы
делаются с определённой периодичностью, загружаются в файл, а позже предоставляются пользователю из этого файла.
За это отвечает класс DataCacher.
Он предоставляет базовый функционал для загрузки и кэширования данных в файл.
Его наследники - TickersDataCacher и IndicesDataCacher - представляют уже кэширование конкретных
данных.
Их методы load_data() будут вызываться с определённой частотой с помощью библиотеки APScheduler.
За настройку APScheduler будет отвечать класс Scheduler, который будет управлять частотой загрузки этих данных.

## Запросы к API

Данные можно получать по двум адресам:

1. `/api`: метод POST, принимает на вход JSON в формате:
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
2. `/api/tickers/<ticker>/chart`: метод POST, принимает на вход JSON в формате:
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
3. `/api/tickers/<ticker>/values`: метод POST, ничего не принимает на вход.
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
4. `/api/categories`: метод POST, ничего не принимает на вход.
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
