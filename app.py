from flask import Flask, request, jsonify, render_template, redirect
from challenge import fun_add_mission_wait, fun_add_detail, fun_read_message, fun_complete_mission, fun_del_mission_wait, fun_deny_mission_wait, fun_add_mission
from score import fun_score_change, fun_buy_card
from note import fun_add_note, fun_update_moon
from home import fun_add_home, fun_add_user, fun_set_love_day
from login import fun_login
from search_data import fun_find_data
import json
from flask_cors import *
from wechatbot import fun_add_user, find_all_user, update_onel_user, find_all_data, update_all_data, find_my_data

app = Flask(__name__)
CORS(app, supports_credentials=True)

# 读取参数
def load_arg(request):
    try:
        arg = json.loads(request.get_data())
    except:
        arg = {}
    return arg

# 构造返回
def get_result(result):
    if type(result)==bool:
        return jsonify({"ok":result})
    elif type(result)==dict:
        result['_id'] = str(result["_id"])
        return jsonify(({"ok":True, "data": result}))
    elif type(result)==list:
        for i in result:
            i['_id'] = str(i["_id"])
        return jsonify(({"ok": True, "data": result}))
    else:
        return jsonify(({"ok": True, "data": result}))


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



# 下面是骰子用的
@app.route('/coc', methods=['GET'])
def coc_new_card():
    return render_template("index.html")
@app.route('/admin', methods=['GET'])
def coc_admin():
    return render_template("admin.html")
@app.route('/api/coc_new', methods=['POST'])
def api_coc_new_card():
    arg = load_arg(request)
    result = fun_add_user(arg)
    if result:
        return jsonify({"ok": True, "data": "aaaaaaaaaaaa"})
    else:
        return jsonify({"ok": False, "data": "aaaaaaaaaaaa"})

@app.route('/api/get_all_user', methods=['POST'])
def api_coc_all_user():
    arg = load_arg(request)
    group = arg["group"]
    result = find_all_user(group)
    return jsonify(({"data": result}))


@app.route('/api/get_all_data', methods=['GET'])
def api_coc_get_all_data():
    result = find_all_data()
    return jsonify(({"data": result}))

@app.route('/api/get_my_data', methods=['POST'])
def api_coc_get_my_data():
    arg = load_arg(request)
    user = arg["user"]
    group = arg['group']
    result = find_my_data(group, user)
    return jsonify({"data": result})

@app.route('/api/coc_update_user', methods=['POST'])
def api_coc_update_user():
    arg = load_arg(request)
    result = update_onel_user(arg)
    return jsonify(({"ok": result}))

@app.route('/api/coc_update_all_data', methods=['POST'])
def api_coc_update_all_data():
    arg = load_arg(request)
    result = update_all_data(arg)
    return jsonify(({"ok": result}))


@app.route('/_next/<path:subpath>')
def get_redirect(subpath):
    print("重定向！")
    return redirect('/static/_next/'+subpath, code=302, Response=None)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7684)
