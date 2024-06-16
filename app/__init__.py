from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Wichtig für Flask-Formulare und Sessions

    from . import routes
    app.register_blueprint(routes.bp)

    return app
