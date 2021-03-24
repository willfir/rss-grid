from flask import Flask
from aggregator import aggregator_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(aggregator_bp)

    return app
