from flask import Flask

from api import simple_api


def create_app():
    app = Flask(__name__)

    app.register_blueprint(simple_api)

    return app

app = create_app()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
