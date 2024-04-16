from flask import Flask, request, jsonify, render_template, redirect, Blueprint
from util import load_arg
from flask_cors import *
from app.ourlove import app as app_api
from app.wedice import wedice

app = Flask(__name__)
CORS(app, supports_credentials=True)
# app.register_blueprint(create(), url_prefix="/")
# bp = Blueprint("ourlove", __name__)
app.register_blueprint(app_api, url_prefix="/")
app.register_blueprint(wedice, url_prefix="/api")

# 下面是骰子用的
@app.route('/coc', methods=['GET'])
def coc_new_card():
    return render_template("index.html")

@app.route('/show', methods=['GET'])
def coc_show_card():
    return render_template("show.html")


@app.route('/self', methods=['GET'])
def coc_self_admin():
    return render_template("self.html")
@app.route('/admin', methods=['GET'])
def coc_admin():
    return render_template("admin.html")


@app.route('/_next/<path:subpath>')
def get_redirect(subpath):
    # print("重定向！")
    return redirect('/static/_next/'+subpath, code=302, Response=None)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7684)
