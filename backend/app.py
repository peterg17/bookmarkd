import os
from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
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
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# set up logging
logging.basicConfig(format="[%(filename)s:%(lineno)d]\t %(message)s")
log = logging.getLogger(__name__)
log.setLevel("INFO")

db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role")

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %r>" % self.username


API = Blueprint("", __name__)


@API.route("/")
def index():
    return "<h1>Bookmarkd Landing Page</h1>"


@API.route("/upload", methods=["POST"])
def upload():
    log.info("\n\n-----------------------------------------")
    log.info("Uploading Bookmarks\n")
    formKeys = request.form.keys()
    file_name = request.form["filename"]
    log.info("name is: " + file_name)
    # file_type = request.form["filetype"]
    # file_text = request.form["filedata"]
    return jsonify(success=True)


app.register_blueprint(API, url_prefix="/")
