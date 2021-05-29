import os
from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging

POSTGRES = {
    "user": "postgres",
    "pw": "",
    "db": "db",
    "host": "localhost",
    "port": "5432",
}

SQLALCHEMY_DATABASE_URI = (
    "postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s"
    % POSTGRES
)

basedir = os.path.abspath(os.path.dirname(__file__))


# set up logging
logging.basicConfig(format="[%(filename)s:%(lineno)d]\t %(message)s")
log = logging.getLogger(__name__)
log.setLevel("INFO")

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .api import API

    CORS(API)
    app.register_blueprint(API, url_prefix="/api/v1")

    return app
