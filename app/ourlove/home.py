from database import mydb
from database import ColHome, ColUser, ColHomeMembers


# 加入空间
def fun_add_home(arg):
    # home_name, home_id
    home_name = arg["home_name"]
    open_id = arg["open_id"]
    # 判断是否在空间中
    if len(list(mydb[ColHome].find({"_openid": open_id})))>0:
        return False
    else:
        # 没有此名字的空间，开始创建
        ress = list(mydb[ColHomeMembers].find({"home_name": home_name, "status": 0}))
        if len(ress)==0:
            res = mydb[ColHomeMembers].insert_one({
                "home_name": home_name,
                "members": [open_id],
                "status": 0
            })
            if res:
                if mydb[ColHome].insert_one({
                    "_id": open_id,
                    "homeid": home_name,
                    "points": 0,
                    "userid_cp": "",
                }):
                    return True
            return False
        # 有此名字的加入空间
        elif len(ress)==1:
            userid_cp = ress[0]["members"][0]
            if mydb[ColHomeMembers].update_one({"_id":ress[0]["_id"]},
                                                {'$set':
                                                    {
                                                        "members": [userid_cp, open_id],
                                                        "status": 1
                                                    }
                                                }):
                if mydb[ColHome].insert_one({
                    "_id": open_id,
                    "homeid": home_name,
                    "points": 0,
                    "userid_cp": userid_cp,
                }):
                    if mydb[ColHome].update_one({"_id": userid_cp}, {'$set':{userid_cp: open_id}}):
                        return True
            return False
        else:
            return False


# 添加用户
def fun_add_user(arg):
    # userinfo, avatarUrl, gender
    userinfo = arg["userinfo"]
    avatarUrl = arg["avatarUrl"]
    gender = arg["gender"]
    open_id = arg["open_id"]
    db = mydb[ColUser]
    reslen = len(list(db.find({"_openid": open_id})))
    # 如果不存在
    if reslen==0:
        db.insert_one({
            "_openid": open_id,
            "userinfo": userinfo,
            "avatarUrl": avatarUrl,
            "gender": gender
        })
        return True
    # 如果存在则修改
    elif reslen==1:
        db.update_one({"_openid": open_id}, {'$set':{
            "userinfo": userinfo,
            "avatarUrl": avatarUrl,
            "gender": gender
        }})
        return True
    else:
        return False

def fun_set_love_day(arg):
    open_id = arg['open_id']
    falltime = arg['time']
    _id = arg["id"]
    res = list(mydb[ColHomeMembers].find({"home_name":_id}))
    if len(res)!=1:
        return False
    if open_id==res[0]['members'][0] or open_id==res[0]['members'][1]:
        mydb[ColHomeMembers].update_one({"home_name": _id}, {'$set':{
            "FallInLoveTime": falltime,
        }})
    return True


