# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS

from conf.config import *
from auth.login import login_manager
from blueprint.product_bp import bp as product_bp
from blueprint.login_bp import bp as login_bp
from blueprint.task2_bp import bp as task_bp2
from blueprint.task3_bp import bp as task_bp3
from blueprint.task4_bp import bp as task_bp4
from blueprint.task5_bp import bp as task_bp5
from blueprint.olt_bp import bp as olt_bp

from flask import render_template

app = Flask(__name__,
static_folder='./dist/static',
template_folder = "./dist")

#app = Flask(__name__)
CORS(app, resources=CORS_RESOURCES)

app.secret_key = APP_SECRETE_KEY
login_manager.init_app(app)
app.register_blueprint(login_bp)
app.register_blueprint(product_bp)
app.register_blueprint(task_bp2)
app.register_blueprint(task_bp3)
app.register_blueprint(task_bp4)
app.register_blueprint(task_bp5)
app.register_blueprint(olt_bp)

@app.route('/')
def index():
    return render_template('index.html',name='index')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
