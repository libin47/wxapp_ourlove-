from database import ColGame, dicedb
import time
import pymongo


def update_onel_user(data):
    userid = data["wxid"]
    groupid = data["group"]
    res = list(dicedb[ColGame].find({"_id": groupid}))
    if len(res)==0:
        return {"ok": False}
    else:
        d = res[0][userid]
        d["HP"] = data["HP"]
        d["MP"] = data["MP"]
        d["SAN"] = data["SAN"]
        dicedb[ColGame].update_one({"_id":groupid},{
            "$set":{
                userid: d
            }})
        return True

def fun_add_user(data):
    userid = data["user"]
    groupid = data["group"]
    card = data['data']
    res = list(dicedb[ColGame].find({"_id": groupid}))
    if(len(res)) == 0:
        dicedb[ColGame].insert_one({
            "_id": groupid,
            "status": True,
            "Gaming": "pause",
            userid: card
        })
    else:
        r = res[0]
        r[userid] = card
        dicedb[ColGame].update_one({"_id":groupid},{
            "$set":{
                userid: card
            }})
    return True


def find_all_user(group):
    res = list(dicedb[ColGame].find({"_id": group}))
    if len(res) == 1:
        return res[0]
    else:
        return False


def find_all_data():
    res = list(dicedb[ColGame].find())
    return res


def update_all_data(data):
    for key in data.keys():
        res = list(dicedb[ColGame].find({"_id": key}))
        if len(res) == 1:
            updata = {}
            for dkey in data[key].keys():
                updata[dkey] = data[key][dkey]
            dicedb[ColGame].update_one({"_id":key}, {"$set": updata})
        elif len(res) == 0:
            indata = data[key]
            indata['_id'] = key
            dicedb[ColGame].insert_one(indata)
        else:
            dicedb[ColGame].delete_many({"_id":key})
            indata = data[key]
            indata['_id'] = key
            dicedb[ColGame].insert_one(indata)
    return True