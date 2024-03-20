from flask import Flask
from routes.details_page import blueprint as details_blueprint
from routes.main_page import blueprint as main_blueprint
from moex_api.tickers_data_loader import tickers_data_loader
from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler(daemon=True)
# scheduler.add_job(tickers_data_loader, 'interval', minutes=5)
# scheduler.start()
# tickers_data_loader()

application = Flask(__name__)

# register routes
application.register_blueprint(details_blueprint)
application.register_blueprint(main_blueprint)

@application.route("/")
def ping():
    return "hello!", 200

if __name__ == "__main__":
    application.run()
