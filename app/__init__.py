from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin

import logging

from app.config import Paths
from app.routes.main_page import blueprint as chart_blueprint
from app.routes.values import blueprint as values_blueprint
from app.routes.chart import blueprint as main_blueprint
from app.routes.categories import blueprint as categories_blueprint
from app.financial.scheduler import Scheduler


def create_app():
    application = Flask(__name__)

    CORS(application, origins=["http://localhost:8080"], send_wildcard=True)
    logging.getLogger('flask_cors').level = logging.DEBUG

    # logging.basicConfig(filename=Paths.log_path, level=logging.DEBUG)

    # register routes
    application.register_blueprint(chart_blueprint)
    application.register_blueprint(values_blueprint)
    application.register_blueprint(main_blueprint)
    application.register_blueprint(categories_blueprint)

    # register scheduler for loading data
    # scheduler = Scheduler()
    # scheduler.start()

    @application.route('/')
    @application.route('/tickers/<ticker>')
    def main_page(**kwargs):
        return send_from_directory("../client/dist", 'index.html')

    @application.route('/images/<path:path>')
    def send_images(path):
        return send_from_directory("../" + Paths.images_path, path)

    @application.route('/<path:path>')
    def send_static_files(path):
        return send_from_directory("../client/dist", path)

    return application
