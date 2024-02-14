import os
from flask import Flask
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_smorest import Api
from bookingapp.resources import UserBlueprint, BookingBlueprint, ItemBlueprint
import pymysql
pymysql.install_as_MySQLdb()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    db_uri = 'sqlite:///' + os.path.join(app.instance_path, 'bookingapp.sqlite')
    if os.getenv('DOCKER_ENV'):
        with open(os.getenv('DB_PASSWORD_FILE'), 'r') as password_file:
            DB_PASSWORD = password_file.read().strip()

        db_uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{DB_PASSWORD}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

    app.config.from_mapping(
        API_TITLE="Booking REST API",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.3",
        OPENAPI_URL_PREFIX="/",
        OPENAPI_JSON_PATH="/static/json/",
        OPENAPI_SWAGGER_UI_PATH="/docs",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from bookingapp.db import db
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.cli.command("create_db")
    def create_db():
        db.create_all()
        print("Datenbank erstellt!")

    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(BookingBlueprint)

    return app
