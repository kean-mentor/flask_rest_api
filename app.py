from flask import Flask

from utils import storage


def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config['TESTING'] = True
        store_path = "test_file_storage.txt"
    else:
        store_path = "api_file_storage.txt"
    app.config['STORE_PATH'] = store_path
    storage.init_data(store_path)

    from api import simple_api
    app.register_blueprint(simple_api)

    return app


app = create_app()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
