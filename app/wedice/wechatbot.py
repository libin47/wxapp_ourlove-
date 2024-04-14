from database import ColGroup, ColUser, ColPc, dicedb, ColGame
from bson import ObjectId

# 新建卡
def _add_card(userid, card):
    # 插入角色表
    if "_id" in card.keys():
        card.pop("_id")
    card['owner'] = userid
    pcid = dicedb[ColPc].insert_one(card)
    pcid = pcid.inserted_id
    # 更新用户表
    res = list(dicedb[ColUser].find({"wxid": userid}))
    if len(res)==0:
        dicedb[ColUser].insert_one({"wxid": userid, "pc": [str(pcid)]})
    else:
        pclist = res[0]['pc']
        pclist.append(str(pcid))
        dicedb[ColUser].update_one({"wxid": userid}, {"$set": {"pc": pclist}})
    return str(pcid)


# 新建群组模板卡,admin的是公开模板
def _add_tem_card(groupid, card):
    card['owner'] = "group"
    # 插入角色表
    pcid = dicedb[ColPc].insert_one(card)
    pcid = pcid.inserted_id
    # 更新用户表
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    if (len(res)) == 0:
        dicedb[ColGroup].insert_one({
            "_id": groupid,
            "status": True,
            "Gaming": "pause",
            "card": {},
            "group_card": [str(pcid)],
            "config": {}
        })
    else:
        card = res[0]["group_card"]
        card.append(str(pcid))
        dicedb[ColGroup].update_one({"_id": groupid}, {"$set": {"group_card": card}})
    dicedb[ColPc].update_one({"_id": ObjectId(pcid)}, {"$set": {"group": groupid}})
    return True


# 更新卡
def _update_card(card, card_id):
    # 查询角色表
    res = list(dicedb[ColPc].find({"_id": ObjectId(card_id)}))
    if len(res)==0:
        return
    # 更新角色表
    card.pop("_id")
    dicedb[ColPc].update_one({"_id": ObjectId(card_id)}, {"$set": card})
    return True


# 查询多卡,{wxid:id,wxid:id)
def _find_cards(pc):
    result = {}
    for wxid in pc.keys():
        res = list(dicedb[ColPc].find({"_id": ObjectId(pc[wxid])}))
        if len(res)>0:
            r = res[0]
            r["_id"] = str(r["_id"])
            result[wxid] = r
        else:
            result[wxid] = {}
    return result


# 查询单卡
def _find_card(pcid):
    res = list(dicedb[ColPc].find({"_id": ObjectId(pcid)}))
    if len(res)>0:
        r = res[0]
        r["_id"] = str(r["_id"])
        return r
    else:
        return {}


# 群组设置
def fun_group_config(data):
    groupid = data["group"]
    config = data["config"]
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    if len(res)==0:
        dicedb[ColGroup].insert_one({
            "_id": groupid,
            "status": True,
            "Gaming": "pause",
            "card": {},
            "group_card": [],
            "config": config
        })
    else:
        dicedb[ColGroup].update_one({"_id": groupid}, {"$set": {"config": config}})
    return True


def fun_group_status(data):
    groupid = data["group"]
    status = data["status"]
    Gaming = data["Gaming"]
    result = dicedb[ColGroup].update_one({"_id": groupid}, {"$set": {"status": status, "Gaming": Gaming}})
    return True


def fun_group_find_config(data):
    groupid = data["group"]
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    if len(res)==0:
        return False
    else:
        result = res[0]["config"]
        return result

# 群组中
# 新建卡：新建，关联群组
def fun_group_add_user(data):
    userid = data["user"]
    groupid = data["group"]
    card = data['data']
    # 插入角色表
    pcid = _add_card(userid, card)
    # 更新群组表
    if groupid:
        res = list(dicedb[ColGroup].find({"_id": groupid}))
        if (len(res)) == 0:
            dicedb[ColGroup].insert_one({
                "_id": groupid,
                "status": True,
                "Gaming": "pause",
                "card": {userid: pcid},
                "group_card": [],
                "config":{}
            })
        else:
            card = res[0]["card"]
            if userid in card.keys() and card[userid]!="":
                try:
                    dicedb[ColPc].update_one({"_id": ObjectId(card[userid])}, {"$set": {"group": ""}})
                except:
                    pass
            card[userid] = pcid
            dicedb[ColGroup].update_one({"_id": groupid}, { "$set": {"card": card}})
        dicedb[ColPc].update_one({"_id": ObjectId(pcid)}, {"$set": {"group": groupid}})
    return True


# 新建群组的模板卡
def fun_group_add_tem_card(data):
    groupid = data["group"]
    card = data['data']
    return _add_tem_card(groupid, card)


# 删除群组的模板卡
def fun_group_del_tem_card(data):
    groupid = data["group"]
    cardid = data['card_id']
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    if (len(res)) == 0:
        return False
    else:
        dicedb[ColPc].delete_one({"_id": ObjectId(cardid)})
        card = res[0]["group_card"]
        card.remove(cardid)
        dicedb[ColGroup].update_one({"_id": groupid}, {"$set": {"group_card": card}})
        return True


# 更新卡：更新
def fun_group_update_user(data):
    card = data['data']
    card_id = data['card_id']
    return _update_card(card, card_id)


# 查询，所有内容
def fun_find_group_all(data):
    groupid = data["group"]
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    if len(res)>0:
        result = res[0]
        result['card'] = _find_cards(result['card'])
        return result
    else:
        return False


# 查询状态
def fun_find_group_status(data):
    groupid = data["group"]
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    if len(res)>0:
        res = res[0]
        res.pop("_id")
        return res
    else:
        return False


# 查询指定角色信息
def fun_find_group_user(data):
    userid = data["user"]
    groupid = data["group"]
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    if len(res)>0:
        if userid in res[0]['card'].keys():
            result = _find_card(res[0]['card'][userid])
            return result
        else:
            return {}
    else:
        return False


# 根据微信id查询所有卡
def fun_find_user(data):
    userid = data["user"]
    groupid = data["group"]
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    result_group = {}
    group_card_id = ""
    if len(res)>0:
        if userid in res[0]['card'].keys():
            group_card_id = res[0]['card'][userid]
            result_group = _find_card(group_card_id)
    result_all = []
    res = list(dicedb[ColUser].find({"wxid": userid}))
    if len(res)>0:
        if len(res[0]["pc"])>0:
            for pcid in res[0]["pc"]:
                if pcid!=group_card_id:
                    result_all.append(_find_card(pcid))
    return {"user_group": result_group, "user": result_all}


def fun_find_one_card(data):
    card_id = data['card_id']
    return _find_card(card_id)


# 查询所有模板卡
def fun_find_group_tem_card(data):
    groupid = data["group"]
    res = list(dicedb[ColGroup].find({"_id": groupid}))
    if len(res)>0:
        cardlist = res[0]["group_card"]
        result1 = []
        for pcid in cardlist:
            result1.append(_find_card(pcid))
    else:
        result1 = []
    res = list(dicedb[ColGroup].find({"_id": "admin"}))
    if len(res)>0:
        cardlist = res[0]["group_card"]
        result2 = []
        for pcid in cardlist:
            result2.append(_find_card(pcid))
    else:
        result2 = []
    return {"group": result1, "admin": result2}


# 私聊
# 新建卡
def fun_self_add_user(data):
    id = data["id"]
    res = list(dicedb[ColUser].find({"_id": ObjectId(id)}))
    if len(res)==0:
        return False
    else:
        wxid = res[0]["wxid"]
        pcid = _add_card(wxid, data["data"])
        return True


# 查询卡
def fun_self_find_user(data):
    id = data["id"]
    res = list(dicedb[ColUser].find({"_id": ObjectId(id)}))
    if len(res)==0:
        return False
    else:
        pcs = res[0]["pc"]
        result = []
        for pc in pcs:
            result.append(_find_card(pc))
        return result


# 更新卡
def fun_self_update_user(data):
    return fun_group_update_user(data)


# 删除卡
def fun_self_del_user(data):
    id = data["id"]
    cardid = data["card_id"]
    res = list(dicedb[ColUser].find({"_id": ObjectId(id)}))
    if (len(res)) == 0:
        return False
    else:
        # 组里取消关联
        pc = _find_card(cardid)
        if 'group' in pc.keys() and pc['group']!="":
            g = list(dicedb[ColGroup].find({"_id": pc['group']}))[0]
            c = g['card']
            for wxid in c.keys():
                if c[wxid] == cardid:
                    c.pop(wxid)
            dicedb[ColGroup].update_one({"_id": pc['group']}, {"$set": {"card": c}})
        # 删除数据
        dicedb[ColPc].delete_one({"_id": ObjectId(cardid)})
        # 更新个人关联
        card = res[0]["pc"]
        card.remove(cardid)
        dicedb[ColUser].update_one({"_id": ObjectId(id)}, {"$set": {"pc": card}})
        return True


# 通过wxid获取id
def fun_self_find_id_by_wxid(data):
    wxid = data["user"]
    res = list(dicedb[ColUser].find({"wxid": wxid}))
    if len(res)==0:
        id = dicedb[ColUser].insert_one({"wxid": wxid, "pc": []})
        return str(id.inserted_id)
    else:
        return str(res[0]["_id"])


def trans_old():
    # 转换旧的数据
    res = list(dicedb[ColGame].find())
    for r in res:
        rlist = list(r.keys())
        group = r["_id"]
        if group == "admin":
            rlist.remove("status")
            rlist.remove("Gaming")
            rlist.remove("_id")
            for key in rlist:
                fun_group_add_tem_card({ "group": group, "data": r[key]})
        else:
            rlist.remove("status")
            rlist.remove("Gaming")
            rlist.remove("_id")
            for key in rlist:
                user = key
                fun_group_add_user({"user": user, "group": group, "data": r[key]})
    return True