from database import ColGroup, ColUser, ColPc, dicedb, ColGame
from bson import ObjectId

# 获取群组，没有则新建
def _find_group(group):
    res = list(dicedb[ColGroup].find({"_id": group}))
    if len(res)==0:
        dicedb[ColGroup].insert_one({
            "_id": group,
            "status": True,
            "Gaming": "pause",
            "card": {},
            "group_card": [],
            "config": {}
        })
        return list(dicedb[ColGroup].find({"_id": group}))[0]
    else:
        return res[0]

# 新建卡
def _add_card(userid, card):
    # 插入角色表
    if "_id" in card.keys():
        card.pop("_id")
    card['owner'] = userid
    card["group"] = []
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
    res_group = _find_group(groupid)
    card = res_group["group_card"]
    card.append(str(pcid))
    dicedb[ColGroup].update_one({"_id": groupid}, {"$set": {"group_card": card}})
    dicedb[ColPc].update_one({"_id": ObjectId(pcid)}, {"$set": {"group": [groupid]}})
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

# 关联卡
def _link_card(group, wxid, cardid):
    res_group = _find_group(group)
    cards = res_group["card"]
    if wxid in cards.keys() and cards[wxid]:
        cardid_old = cards[wxid]
        _unlink_card(group, wxid, cardid_old)
        return _link_card(group, wxid, cardid)
    else:
        card = _find_card(cardid)
        if card.keys():
            groups = card["group"] if "group" in card.keys() else []
            if type(groups)==str:
                groups = [groups]
            groups.append(group)
            dicedb[ColPc].update_one({"_id": ObjectId(cardid)},{"$set": {"group": groups}})
            cards[wxid] = cardid
            dicedb[ColGroup].update_one({"_id": group}, {"$set" : {"card": cards}})
            return True
        else:
            return False


# 取消关联卡
def _unlink_card(group, wxid, cardid):
    res_group = _find_group(group)
    cards = res_group["card"]
    if wxid in cards.keys() and cards[wxid]:
        cards[wxid] = ""
        dicedb[ColGroup].update_one({"_id": group}, {"$set" : {"card": cards}})
    res_card = _find_card(cardid)
    if res_card.keys():
        groups = res_card["group"] if "group"in res_card.keys() else []
        if type(groups) == str:
            groups = [groups]
        groups.remove(group)
        dicedb[ColPc].update_one({"_id": ObjectId(cardid)}, {"$set" : {"group": groups}})
    return True



# 群组设置
def fun_group_config(data):
    groupid = data["group"]
    config = data["config"]
    res = _find_group(groupid)
    dicedb[ColGroup].update_one({"_id": groupid}, {"$set": {"config": config}})
    return True


def fun_group_status(data):
    groupid = data["group"]
    status = data["status"]
    Gaming = data["Gaming"]
    res = _find_group(groupid)
    dicedb[ColGroup].update_one({"_id": groupid}, {"$set": {"status": status, "Gaming": Gaming}})
    return True


def fun_group_find_config(data):
    groupid = data["group"]
    res = _find_group(groupid)
    return res["config"]

# 群组中
# 新建卡：新建，关联群组
def fun_group_add_user(data):
    userid = data["user"]
    groupid = data["group"]
    card = data['data']
    # 插入角色表
    pcid = _add_card(userid, card)
    return _link_card(groupid, userid, pcid)



# 新建群组的模板卡
def fun_group_add_tem_card(data):
    groupid = data["group"]
    card = data['data']
    return _add_tem_card(groupid, card)


# 删除群组的模板卡
def fun_group_del_tem_card(data):
    groupid = data["group"]
    cardid = data['card_id']
    res = _find_group(groupid)
    dicedb[ColPc].delete_one({"_id": ObjectId(cardid)})
    card = res["group_card"]
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
    result = _find_group(groupid)
    result['card'] = _find_cards(result['card'])
    return result

# 查询状态
def fun_find_group_status(data):
    groupid = data["group"]
    result = _find_group(groupid)
    return result


# 查询指定角色信息
def fun_find_group_user(data):
    userid = data["user"]
    groupid = data["group"]
    res = _find_group(groupid)
    if userid in res['card'].keys() and res['card'][userid]:
        result = _find_card(res['card'][userid])
        return result
    else:
        return {}


# 链接一张卡
def fun_link_group_user(data):
    userid = data["user"]
    card_id = data["card_id"]
    groupid = data["group"]
    return _link_card(groupid, userid, card_id)


# 根据微信id查询所有卡
def fun_find_user(data):
    userid = data["user"]
    groupid = data["group"]
    res = _find_group(groupid)
    result_group = {}
    group_card_id = ""
    if userid in res['card'].keys() and res['card'][userid]:
        group_card_id = res['card'][userid]
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
    result1 = []
    res = _find_group(groupid)
    cardlist = res["group_card"]
    for pcid in cardlist:
        result1.append(_find_card(pcid))
    res = _find_group("admin")
    result2 = []
    cardlist = res["group_card"]
    for pcid in cardlist:
        result2.append(_find_card(pcid))
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
        wxid = res[0]["wxid"]
        # 组里取消关联
        pc = _find_card(cardid)
        if 'group' in pc.keys() and pc['group']:
            for g in pc["group"]:
                _unlink_card(g, wxid, cardid)
            return fun_self_del_user(data)
        else:
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