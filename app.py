from flask import Flask
from routes.chart import blueprint as chart_blueprint
from routes.values import blueprint as values_blueprint
from routes.main_page import blueprint as main_blueprint
from moex_api.tickers_data_loader import tickers_data_loader
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from datetime import datetime

logging.basicConfig(filename="storage/debug.log", level=logging.DEBUG)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(tickers_data_loader, 'interval', minutes=10, start_date=datetime.now())
scheduler.start()

tickers_data_loader()

application = Flask(__name__)

# register routes
application.register_blueprint(chart_blueprint)
application.register_blueprint(values_blueprint)
application.register_blueprint(main_blueprint)


@application.route("/")
def ping():
    return "hello!", 200


if __name__ == "__main__":
    application.run()
