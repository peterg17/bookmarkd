from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from models import *

app = create_app()
migrate = Migrate(app, db)