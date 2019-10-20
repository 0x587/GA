#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0408@192.168.0.202:3306/GA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
