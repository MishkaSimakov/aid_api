from flask import Blueprint, send_from_directory
from app import Paths

blueprint = Blueprint('static', __name__)


@blueprint.route('/')
@blueprint.route('/tickers/<ticker>')
def main_page(**kwargs):
    """
    Путь, по которому можно получить html-страницы сайта.
    На стороне клиента используется vue router, поэтому по всем путям, доступным для пользователя
    мы возвращаем основную html-страницу, а на ней vue router уже сам разбирается.
    """
    return send_from_directory(Paths.get_client_path("dist"), 'index.html')


@blueprint.route('/images/<path:path>')
def send_images(path):
    """
    Путь, по которому можно получить изображение, хранящееся на сервере.
    Сейчас по этому пути можно получать только иконки для тикеров.
    """

    return send_from_directory(Paths.images_path, path)


@blueprint.route('/<path:path>')
def send_static_files(path):
    """
    Путь, по которому можно получить js и css, необходимые для работы клиентской стороны сайта.
    """

    return send_from_directory(Paths.get_client_path("dist"), path)
