from app.ourlove import app as app_api
from app.wedice import wedice
from flask import Blueprint

def create():
    bp = Blueprint("ourlove", __name__)
    bp.register_blueprint(app_api, url_prefix="/")
    bp.register_blueprint(wedice, url_prefix="/api")
    return bp