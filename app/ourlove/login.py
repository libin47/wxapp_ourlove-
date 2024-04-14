import requests
import json
def fun_login(arg):
    payload = {
        "appid": "wxecfe12d572efdfad",
        "secret": "35c3c50f3f8ee2d470572c4f4098f5f1",
        "js_code": arg["code"],
        "grant_type": "authorization_code"
    }
    res = requests.get(url='https://api.weixin.qq.com/sns/jscode2session?appid=wxecfe12d572efdfad&secret=35c3c50f3f8ee2d470572c4f4098f5f1&js_code=%s&grant_type=authorization_code'%arg["code"])
    res = json.loads(res.text)
    # print(res)
    
    return res["openid"]