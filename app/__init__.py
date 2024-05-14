from flask import Flask
from flask_cors import CORS
import logging
from app.config import Paths
from app.financial.DataSourcesContainer import DataSourcesContainer

from app.financial.scheduler import Scheduler
from app.routes import register_blueprints


def create_app():
    """Основная функция, которая создаёт приложение и настраивает его."""

    DataSourcesContainer.init_sources()

    application = Flask(__name__)
    application.url_map.strict_slashes = False

    if application.debug:
        # необходимо для разработки интерфейса
        CORS(application, origins=["http://localhost:8080"], send_wildcard=True)

    logging.getLogger('flask_cors').level = logging.DEBUG

    # logging.basicConfig(filename=Paths.log_path, level=logging.DEBUG)

    register_blueprints(application)

    scheduler = Scheduler()
    scheduler.start()

    return application
