from flask import Flask
from flask_cors import CORS

from conf.config import HOST, PORT, CORS_RESOURCES
from blueprint.olt_bp import bp as obp
from blueprint.aaa_bp import bp as abp

app = Flask(__name__)
CORS(app, resources=CORS_RESOURCES)

app.register_blueprint(obp)
app.register_blueprint(abp)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
