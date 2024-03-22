from flask import Flask
from app.routes.main_page import blueprint as chart_blueprint
from app.routes.values import blueprint as values_blueprint
from app.routes.chart import blueprint as main_blueprint
from app.financial.scheduler import Scheduler
import logging


# logging.basicConfig(filename="../storage/debug.log", level=logging.DEBUG)

def create_app():
    application = Flask(__name__)

    # register routes
    application.register_blueprint(chart_blueprint)
    application.register_blueprint(values_blueprint)
    application.register_blueprint(main_blueprint)

    # register scheduler for loading data
    scheduler = Scheduler()
    scheduler.start()

    @application.route("/")
    def ping():
        return "hello!", 200

    return application
