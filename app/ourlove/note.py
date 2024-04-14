from database import mydb, ColNotebook, ColHome, ColHomeMembers, ColMoonDead
import time
import pymongo

def fun_add_note(arg):
    # print(arg)
    open_id = arg["open_id"]
    _id = arg['id']
    note = arg['note']
    title = arg['title']
    auto = arg['auto']
    homeid = arg["homeid"]
    if title=="":
        title = "无标题"
    
    if _id=="":
        if not auto:
            result = mydb[ColNotebook].insert_one({
                '_id' : str(int(time.time()*100000000)),
                'homeid': homeid,
                'userid': open_id,
                'title': title,
                'title_now': "",
                'note': note,
                'note_now': "",
                'creattime': int(time.time()*1000),
                'lasttime': int(time.time()*1000),
                'stauts': 0,
                'old_id': "",
            })
            # print(result)
        return True
    else:
        if auto:
            # 自动更新 不覆盖
            mydb[ColNotebook].update_one({"_id":_id},{
                "$set":{
                    "title_now": title,
                    "note_now": note
                    }})
            return True
        else:
            res = list(mydb[ColNotebook].find({"_id": _id}))[0]
            # 新旧不一样时才会更新
            if res['note']!=note or res['title']!=title:
                mydb[ColNotebook].insert_one({
                    'homeid': homeid,
                    'userid': open_id,
                    'title': res['title'],
                    'title_now': "",
                    'note': res['note'],
                    'note_now': "",
                    'creattime': res['creattime'],
                    'lasttime': res['lasttime'],
                    'stauts': -1,
                    'old_id': res['_id'],
                    })
            mydb[ColNotebook].update_one({"_id":_id},{
                "$set":{
                        'title': title,
                        'title_now': "",
                        'note': note,
                        'note_now': "",
                        'lasttime': int(time.time()*1000),
                    }})
            return True
    

def fun_update_moon(arg):
    homeid = arg['homeid']
    stat = arg['stat']
    
    res = list(mydb[ColMoonDead].find({"homeid":homeid}))
    # 新建
    if stat==0:
        if len(res)==0:
            mydb[ColMoonDead].insert_one({
                'homeid': homeid,
                'moonday': arg['moonday'],
                'durday': arg['durday'],
                'data': [],
            })
            return True
    # 更新条目
    elif stat==1:
        if len(res)==1:
            mydb[ColMoonDead].update_one({"homeid":homeid},{
                "$set":{
                    'moonday': arg['moonday'],
                    'durday': arg['durday'],
                    }
            })    
            return True
    # 更新数据
    elif stat==2:
        if len(res)==1:
            mydb[ColMoonDead].update_one({"homeid":homeid},{
                "$set":{
                    'data': arg['data'],
                    }})
            return True
    # 第一条
    elif stat==3:
        if len(res)==1:
            mydb[ColMoonDead].update_one({"homeid":homeid},{
                "$set":{
                    'basetime': arg['basetime'],
                    'data': arg['data']
                    }})
            return True
    return False  
        
        













