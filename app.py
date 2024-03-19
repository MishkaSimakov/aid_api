from flask import Flask
from routes.details_page import blueprint as details_blueprint
from routes.main_page import blueprint as main_blueprint

application = Flask(__name__)

# register routes
application.register_blueprint(details_blueprint)
application.register_blueprint(main_blueprint)

if __name__ == "__main__":
    application.run(port=8000)
