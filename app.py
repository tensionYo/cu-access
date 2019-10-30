from flask import Flask
from flask_cors import CORS

from conf.config import *
from auth.login import login_manager
from blueprint.product_bp import bp as product_bp
from blueprint.login_bp import bp as login_bp

app = Flask(__name__)
CORS(app, resources=CORS_RESOURCES)

app.secret_key = APP_SECRETE_KEY

login_manager.init_app(app)
app.register_blueprint(login_bp)
app.register_blueprint(product_bp)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
