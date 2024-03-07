from database import mydb, ColChallenge, ColChallengeDetail, ColChallengeDemo, ColChallengeWait, ColHome, ColHomeMembers
import time
import pymongo
from score import fun_score_change

def fun_add_mission(arg):
    open_id = arg["open_id"]
    mission_id = arg["_id"]
    score = arg['score']
    
    score_sum = -1
    
    res = list(mydb[ColChallengeWait].find({"_id":mission_id}))[0]
    if res['people']!=open_id:
        return False
    if res['alone']:
        score_sum = res['score']
        score_all = [res['score']]
    else:
        score_sum = res['score'] + score
        score_all = [res['score'], score]
    mydb[ColChallenge].insert_one({
        '_id': mission_id,
        'homeid': res['homeid'],
        'title': res['title'],
        'title_sub': res['title_sub'],
        'status': 0,
        'pic_file': "",
        'type': res['type'],
        'type_sub': res['type_sub'],
        'alone': res['alone'],
        'score_sum': score_sum,
        'score': score_all,
        'people': res['doitpeople'],
        'creatpeople': res['creatpeople'],
        'daysplit': res['daysplit'],
        'unread': res['creatpeople']
    })
    mydb[ColChallengeDetail].insert_one({
        'homeid': res['homeid'],
        'challenge_id': mission_id,
        'time': int(time.time()*1000),
        'user_id': res['creatpeople'],
        'notes': "创建了任务",
        'pic': "",
        'process': 0
    })
    mydb[ColChallengeWait].delete_one({"_id":  mission_id})
    return True
    

def fun_add_mission_wait(arg):
    open_id = arg["open_id"]
    homeid = arg["homeid"]
    people = arg["people"]
    doitpeople = arg["doitpeople"]
    new_mission_name = arg["new_mission_name"]
    new_mission_sub_name = arg["new_mission_sub_name"]
    alone_mission = arg["alone_mission"]
    new_mission_score = arg["new_mission_score"]
    new_mission_type = arg["new_mission_type"]
    id = arg["id"]
    challenge_id = str(int(time.time()*100000000))
    day = arg["day"]
    
    res = list(mydb[ColHome].find({"_id": open_id}))
    if res[0]["homeid"] != homeid:
        return False
    
    res = list(mydb[ColHomeMembers].find({"home_name": homeid}))
    if res[0]["members"][0] != arg['people'] and res[0]["members"][1] != arg['people']:
        return false
    
    # 个人任务直接创建，对方的需要审核
    if alone_mission and doitpeople[0]==open_id:
        mydb[ColChallenge].insert_one({
            "_id": challenge_id,
            "homeid": homeid,
            "title": new_mission_name,
            "title_sub": new_mission_sub_name,
            "status": 0,
            "pic_file": "",
            "type": new_mission_type,
            "type_sub": 0,
            "alone": True,
            "people": doitpeople,
            "creatpeople": open_id,
            "daysplit": day,
            "score": [0],
            "score_sum": 0,
        })
        mydb[ColChallengeDetail].insert_one({
              "homeid": homeid,
              "challenge_id": challenge_id,
              "time": int(time.time()*1000),
              "user_id": open_id,
              "notes": "创建了任务",
              "pic": "",
              "process": 0
        })
        return True
    else:
        if id == "":
            mydb[ColChallengeWait].insert_one({
              "homeid": homeid,
              "title": new_mission_name,
              "title_sub": new_mission_sub_name,
              "type": new_mission_type,
              "type_sub": 0,
              "alone": alone_mission,
              "score": new_mission_score,
              "creatpeople": open_id,
              "people": people,
              "doitpeople": doitpeople,
              "daysplit": day,
              "_id": challenge_id,
            })
            return True
        else:
            mydb[ColChallengeWait].update_one({"_id":id},{
                "$set":{
                    "homeid": homeid,
                    "title": new_mission_name,
                    "title_sub": new_mission_sub_name,
                    "type": new_mission_type,
                    "type_sub": 0,
                    "alone": alone_mission,
                    "score": new_mission_score,
                    "creatpeople": open_id,
                    "people": people,
                    "doitpeople": doitpeople,
                    "daysplit": day,
                    }})
            return True


def fun_add_detail(arg):
    open_id = arg['open_id']
    mission_id = arg['_id']
    pic = arg['pic']
    notes = arg['notes']
    address = arg['address']
    address_gps = arg['address_gps']
    detail_id = str(int(time.time()*100000000))
    # 数据校对
    res = list(mydb[ColChallenge].find({'_id':mission_id}))
    if len(res)!=1:
        # print("找不到mission")
        return False
    mission = res[0]
    # 检查动态权限
    hm = list(mydb[ColHomeMembers].find({'home_name':mission["homeid"]}))
    if len(hm)==0:
        # print("找不到用户")
        return False
    if not (hm[0]['members'][0]==open_id or hm[0]['members'][1]==open_id):
        # print("用户与任务不匹配")
        return False
    # 提示谁
    cpid = ""
    if mission['alone']:
        if open_id != mission['people'][0]:
            cpid = mission['people'][0]
    else:
        if hm[0]['members'][0] == open_id:
            cpid = hm[0]['members'][1]
        elif hm[0]['members'][1] == open_id:
            cpid = hm[0]['members'][0]
    # 增加未读消息
    mydb[ColChallenge].update_one({"_id":mission_id},{
        "$set":{
            "unread": cpid,
            }})
    # 检查完成/打卡权限
    validclock = False
    # 打卡任务
    if mission['type']==1:
        dres = list(mydb[ColChallengeDetail].find({
            "challenge_id": mission_id,
            "user_id": open_id,
            "process": 1,
        }).sort("time", pymongo.DESCENDING).limit(1))
        if len(dres)==1:
            # 时间够了
            if (int(time.time()*1000) - dres[0]['time'])>(mission['daysplit']-0.5)*24*3600:
                validclock = True
        else:
            validclock = True
        mydb[ColChallengeDetail].insert_one({
            "homeid": mission['homeid'],
            "challenge_id": mission['_id'],
            'time': int(time.time()*1000),
            'user_id': open_id,
            'notes': notes,
            'pic': pic,
            'process': 1 if validclock else 2,
            'address': address,
            'address_gps': address_gps,
        })
        # 打卡成功分数结算
        if validclock:
            if mission['alone']:
                score_delta = mission['score_sum']
            else:
                score_delta = mission['score_sum']//2
            fun_score_change({
                "user_id": open_id,
                "score": score_delta,
                "type": "打卡",
                "challenge_id": mission['_id'],
                "challenge_title": mission['title'],
                "reward_id": "",
                "reward_title": ""
            })
    # 其他任务
    else:
        mydb[ColChallengeDetail].insert_one({
            "homeid": mission['homeid'],
            "challenge_id": mission['_id'],
            'time': int(time.time()*1000),
            'user_id': open_id,
            'notes': notes,
            'pic': pic,
            'process': 1,
            'address': address,
            'address_gps': address_gps,
        })
    return True
                
                
def fun_read_message(arg):
    open_id = arg['open_id']
    mission_id = arg['_id']
    
    mydb[ColChallenge].update_one({"_id":mission_id},{
        "$set":{
            "unread": "",
            }})
    return True
        
        
def fun_complete_mission(arg):
    open_id = arg['open_id']
    mission_id = arg['_id']
    pic = arg['pic']
    # 数据校对
    res = list(mydb[ColChallenge].find({'_id':mission_id, 'status': 0}))
    if len(res)!=1:
        # print("找不到mission")
        return False
    mission = res[0]
    if not (mission['people'][0]==open_id or mission['people'][1]==open_id):
        return False
    cpid = ""
    # pic默认值
    if pic == "":
        pic = "https://image.wind-watcher.cn/96fa716b5c7588615c989c402328f89a"
    # 校验
    hm = list(mydb[ColHomeMembers].find({'home_name': mission['homeid']}))
    # print(hm)
    if len(hm)!=1:
        return False
    if hm[0]['members'][0] == open_id:
        cpid = hm[0]['members'][1]
    elif hm[0]['members'][1] == open_id:
        cpid = hm[0]['members'][0]
    # update_
    mydb[ColChallenge].update_one({"_id":mission_id},{
        "$set":{
            "status": 1,
            "pic_file": pic,
            "unread": cpid
            }})
    # detail添加
    mydb[ColChallengeDetail].insert_one({
        'homeid': mission['homeid'],
        'challenge_id': mission['_id'],
        'time': int(time.time()*1000),
        'user_id': open_id,
        'notes': "完成了任务",
        'pic': "",
        'process': -1,
    })
    # 积分结算
    if mission['type']==1:
        return False
    if mission['alone']:
        if mission['creatpeople']==open_id:
            return False
        fun_score_change({
            "user_id": open_id,
            "score": mission['score_sum'],
            "type": "完成",
            "challenge_id": mission['_id'],
            "challenge_title": mission['title'],
            "reward_id": "",
            "reward_title": ""
        })
    else:
        if mission['type']==0:
            score = mission['score'][1]
        elif mission['type']==1:
            score = 0
        elif mission['type']==2:
            score = mission['score_sum']
        userid = mission['people'][0]
        fun_score_change({
            "user_id": userid,
            "score": score,
            "type": "完成",
            "challenge_id": mission['_id'],
            "challenge_title": mission['title'],
            "reward_id": "",
            "reward_title": ""
        })
        userid = mission['people'][1]
        fun_score_change({
            "user_id": userid,
            "score": score,
            "type": "完成",
            "challenge_id": mission['_id'],
            "challenge_title": mission['title'],
            "reward_id": "",
            "reward_title": ""
        })
    return True
    
def fun_del_mission_wait(arg):
    open_id = arg['open_id']
    mission_id = arg['_id']
    res = list(mydb[ColChallengeWait].find({"_id":  mission_id}))
    if len(res)!=1:
        return False
    if res[0]['creatpeople']!=open_id:
        return False
    mydb[ColChallengeWait].delete_one({"_id":  mission_id})
    return True
    
def fun_deny_mission_wait(arg):
    open_id = arg['open_id']
    mission_id = arg['_id']
    res = list(mydb[ColChallengeWait].find({"_id":  mission_id}))
    if len(res)!=1:
        return False
    if res[0]['people']!=open_id:
        return False
    mydb[ColChallengeWait].update_one({"_id":mission_id},{
        "$set":{
            "people": arg['deny_text']
            }})
    return True
    
    
    
    
    
    
    
    
    
