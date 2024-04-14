from flask import Blueprint
from util import load_arg, get_result
from app.ourlove.challenge import fun_add_mission_wait, fun_add_detail, fun_read_message, fun_complete_mission, fun_del_mission_wait, fun_deny_mission_wait, fun_add_mission
from app.ourlove.score import fun_buy_card
from app.ourlove.note import fun_add_note, fun_update_moon
from app.ourlove.home import fun_add_home, fun_add_user, fun_set_love_day
from app.ourlove.login import fun_login
from app.ourlove.search_data import fun_find_data
from flask import request


app = Blueprint("app", __name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/add_home', methods=['POST'])
def add_home():
    arg = load_arg(request)
    return get_result(fun_add_home(arg))


@app.route('/add_user', methods=['POST'])
def add_user():
    arg = load_arg(request)
    return get_result(fun_add_user(arg))


@app.route('/login', methods=['POST'])
def login():
    arg = load_arg(request)
    return get_result(fun_login(arg))


@app.route('/find_data', methods=['POST'])
def find_data():
    arg = load_arg(request)
    return get_result(fun_find_data(arg))


@app.route('/add_mission', methods=['POST'])
def add_mission():
    arg = load_arg(request)
    return get_result(fun_add_mission(arg))


@app.route('/add_mission_wait', methods=['POST'])
def add_mission_wait():
    arg = load_arg(request)
    return get_result(fun_add_mission_wait(arg))


@app.route('/add_detail', methods=['POST'])
def add_detail():
    arg = load_arg(request)
    r = fun_add_detail(arg)
    return get_result(r)


@app.route('/read_message', methods=['POST'])
def read_message():
    arg = load_arg(request)
    r = fun_read_message(arg)
    return get_result(r)


@app.route('/complete_mission', methods=['POST'])
def complete_mission():
    arg = load_arg(request)
    r = fun_complete_mission(arg)
    return get_result(r)


@app.route('/add_note', methods=['POST'])
def add_note():
    arg = load_arg(request)
    r = fun_add_note(arg)
    return get_result(r)


@app.route('/buy_card', methods=['POST'])
def buy_card():
    arg = load_arg(request)
    r = fun_buy_card(arg)
    return get_result(r)


@app.route('/del_mission_wait', methods=['POST'])
def del_mission_wait():
    arg = load_arg(request)
    r = fun_del_mission_wait(arg)
    return get_result(r)


@app.route('/update_moon', methods=['POST'])
def update_moon():
    arg = load_arg(request)
    r = fun_update_moon(arg)
    return get_result(r)


@app.route('/deny_mission_wait', methods=['POST'])
def deny_mission_wait():
    arg = load_arg(request)
    r = fun_deny_mission_wait(arg)
    return get_result(r)


@app.route('/set_love_day', methods=['POST'])
def set_love_day():
    arg = load_arg(request)
    r = fun_set_love_day(arg)
    return get_result(r)

