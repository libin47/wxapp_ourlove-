from app.wedice.wechatbot import fun_group_add_user, fun_group_add_tem_card,fun_group_del_tem_card,fun_group_update_user,\
    fun_find_group_all,fun_find_group_status,fun_find_user,fun_find_group_tem_card,fun_self_add_user,\
    fun_self_update_user, fun_self_del_user,fun_self_find_id_by_wxid, fun_self_find_user, fun_group_config, fun_group_find_config,\
    fun_find_one_card, trans_old, fun_group_status, fun_find_group_user

from util import load_arg, load_arg_get
from flask import Blueprint
from flask import request,jsonify
wedice = Blueprint("wedice", __name__)


@wedice.route('/coc_group_config', methods=['POST'])
def api_coc_group_config():
    arg = load_arg(request)
    result = fun_group_config(arg)
    return jsonify({"ok": result})


@wedice.route('/coc_group_status', methods=['POST'])
def api_coc_group_post_status():
    arg = load_arg(request)
    result = fun_group_status(arg)
    return jsonify({"ok": result})


@wedice.route('/coc_group_status', methods=['GET'])
def api_coc_group_get_status():
    arg = load_arg_get(request)
    result = fun_find_group_status(arg)
    return jsonify({"data": result})

@wedice.route('/coc_group_config', methods=['GET'])
def api_coc_group_find_config():
    arg = load_arg_get(request)
    result = fun_group_find_config(arg)
    return jsonify({"data": result})


@wedice.route('/coc_group_add_pc', methods=['POST'])
def api_coc_group_add_pc():
    arg = load_arg(request)
    result = fun_group_add_user(arg)
    return jsonify({"ok": result})


@wedice.route('/coc_group_add_tem', methods=['POST'])
def api_coc_group_add_tem():
    arg = load_arg(request)
    result = fun_group_add_tem_card(arg)
    return jsonify({"ok": result})


@wedice.route('/coc_group_del_tem', methods=['POST'])
def api_coc_group_del_tem():
    arg = load_arg(request)
    result = fun_group_del_tem_card(arg)
    return jsonify({"ok": result})


@wedice.route('/coc_group_update', methods=['POST'])
def api_coc_group_update():
    arg = load_arg(request)
    result = fun_group_update_user(arg)
    return jsonify({"ok": result})


@wedice.route('/coc_group_get_all', methods=['POST'])
def api_coc_group_get_all():
    arg = load_arg(request)
    result = fun_find_group_all(arg)
    return jsonify({"data": result})


@wedice.route('/coc_group_get_one', methods=['POST'])
def api_coc_group_get_one():
    arg = load_arg(request)
    result = fun_find_group_user(arg)
    return jsonify({"data": result})


@wedice.route('/coc_group_get_user', methods=['POST'])
def api_coc_group_get_user():
    arg = load_arg(request)
    result = fun_find_user(arg)
    return jsonify({"data": result})


@wedice.route('/coc_get_card', methods=['POST'])
def api_coc_get_card():
    arg = load_arg(request)
    result = fun_find_one_card(arg)
    return jsonify({"data": result})


@wedice.route('/coc_group_get_tem', methods=['POST'])
def api_coc_group_get_tem():
    arg = load_arg(request)
    result = fun_find_group_tem_card(arg)
    return jsonify({"data": result})


@wedice.route('/coc_self_add_pc', methods=['POST'])
def api_coc_self_add_pc():
    arg = load_arg(request)
    result = fun_self_add_user(arg)
    return jsonify({"ok": result})


@wedice.route('/coc_self_update', methods=['POST'])
def api_coc_self_update():
    arg = load_arg(request)
    result = fun_self_update_user(arg)
    return jsonify({"ok": result})

@wedice.route('/coc_self_del_pc', methods=['POST'])
def api_coc_self_del_pc():
    arg = load_arg(request)
    result = fun_self_del_user(arg)
    return jsonify({"ok": result})


@wedice.route('/coc_self_get_id', methods=['POST'])
def api_coc_self_get_id():
    arg = load_arg(request)
    result = fun_self_find_id_by_wxid(arg)
    return jsonify({"data": result})


@wedice.route('/coc_self_get_pc', methods=['POST'])
def api_coc_self_get_pc():
    arg = load_arg(request)
    result = fun_self_find_user(arg)
    return jsonify({"data": result})


@wedice.route('/coc_trans_old', methods=['POST'])
def api_coc_trans_old():
    result = trans_old()
    return jsonify({"ok": result})
