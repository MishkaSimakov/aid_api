from flask import Flask

from app.routes.main_page import blueprint as chart_blueprint
from app.routes.values import blueprint as values_blueprint
from app.routes.chart import blueprint as main_blueprint
from app.routes.categories import blueprint as categories_blueprint
from app.routes.static import blueprint as static_blueprint


def register_blueprints(app: Flask):
    """
    Регистрирует все пути, которые были объявлены в отдельных файлах,
    чтобы они были доступны для объекта app.
    """

    api_blueprints = [
        chart_blueprint, values_blueprint, main_blueprint, categories_blueprint
    ]

    for blueprint in api_blueprints:
        app.register_blueprint(blueprint, url_prefix='/api')

    app.register_blueprint(static_blueprint)
