import json
from flask import Flask, request, jsonify, render_template, redirect

def load_arg(request):
    try:
        arg = json.loads(request.get_data())
    except:
        arg = {}
    return arg

def load_arg_get(request):
    try:
        arg = {}
        for key in request.values.keys():
            arg[key] = request.values.get(key)
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