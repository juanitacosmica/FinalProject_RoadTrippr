from flask import Flask
from config import Config
#init my Database manager


def create_app(config_class=Config):

    # Init the app
    app = Flask(__name__)
    #Link in the Config
    app.config.from_object(config_class)
    # Set Static Directory
    app.static_folder = 'static'
    # Register Bootstrap
    from .views import bp as views_bp

    app.register_blueprint(views_bp)

    return app