from flask import Flask
from routes.chart import blueprint as chart_blueprint
from routes.values import blueprint as values_blueprint
from routes.main_page import blueprint as main_blueprint
from financial.scheduler import Scheduler
import logging

logging.basicConfig(filename="storage/debug.log", level=logging.DEBUG)

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


if __name__ == "__main__":
    application.run()
