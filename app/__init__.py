from flask import Flask
import logging

from app.config import Paths
from app.routes.main_page import blueprint as chart_blueprint
from app.routes.values import blueprint as values_blueprint
from app.routes.chart import blueprint as main_blueprint
from app.routes.categories import blueprint as categories_blueprint
from app.financial.scheduler import Scheduler


def create_app():
    application = Flask(__name__)

    logging.basicConfig(filename=Paths.log_path, level=logging.DEBUG)

    # register routes
    application.register_blueprint(chart_blueprint)
    application.register_blueprint(values_blueprint)
    application.register_blueprint(main_blueprint)
    application.register_blueprint(categories_blueprint)

    # register scheduler for loading data
    scheduler = Scheduler()
    scheduler.start()

    @application.route("/")
    def ping():
        return "hello!", 200

    return application
