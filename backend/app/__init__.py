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

API = Blueprint("", __name__)
CORS(API)


@API.route("/", methods=["GET"])
def index():
    return "<h1>Bookmarkd Landing Page</h1>"


@API.route("/upload", methods=["POST"])
def upload():
    log.info("\n\n-----------------------------------------")
    log.info("Uploading Bookmarks\n")
    # formKeys = request.form.keys()
    # file_name = request.form["filename"]
    json_data = request.json
    log.info("request json is: " + str(json_data))
    # log.info("file name is: " + json_data["filename"])
    # file_type = request.form["filetype"]
    # file_text = request.form["filedata"]
    return jsonify(success=True)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # db.drop_all()
    # db.create_all()
    app.register_blueprint(API, url_prefix="/")

    return app
