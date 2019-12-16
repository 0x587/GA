#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from my_config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')

from UniApp.uniapp import uniapp
app.register_blueprint(uniapp)

from app import models, Routes
import User.UserModel
