from database import mydb, ColChallenge, ColReward, ColHome, ColHomeMembers, ColPoints, ColChallengeDetail
import time
import pymongo

def fun_score_change(arg):
    open_id = arg['user_id']
    score_delta = arg['score']
    stype = arg['type']
    challenge_id = arg['challenge_id']
    challenge_title = arg['challenge_title']
    reward_id = arg['reward_id']
    reward_title = arg['reward_title']
    
    result = list(mydb[ColHome].find({"_id": open_id}))[0]
    score = result['points']
    score = score + score_delta
    mydb[ColHome].update_one({"_id":open_id},{
        "$set":{
            "points": score,
            }})
    mydb[ColPoints].insert_one({
        'userid': open_id,
        'time': int(time.time()*1000),
        'delta': score_delta,
        'type': stype,
        'challenge_id': challenge_id,
        'challenge_title': challenge_title,
        'reward_id': reward_id,
        'reward_title': reward_title
    })
    return score
    
def fun_buy_card(arg):
    open_id = arg['open_id']
    card_id = arg['cardid']
    res = list(mydb[ColReward].find({"_id": card_id}))
    if len(res)!=1:
        return False
    res = res[0]
    ress = list(mydb[ColHome].find({"_id": open_id}))[0]
    cpid = ress['userid_cp']
    homeid = ress['homeid']
    points = ress['points']
    fun_score_change({
        "user_id": open_id,
        "score": -res['price'],
        "type": "兑换",
        "challenge_id": "",
        "challenge_title": "",
        "reward_id": card_id,
        'reward_title': res['title'],
    })
    
    challenge_id = str(int(time.time()*100000000))
    mydb[ColChallenge].insert_one({
        '_id': challenge_id,
        'homeid': homeid,
        'title': res['title'],
        'title_sub': res['title_sub'],
        'status': 0,
        'pic_file': "",
        'type': 3,
        'type_sub': 0,
        'alone': True,
        'score_sum': [0],
        'score': 0,
        'people': [cpid],
        'creatpeople': open_id,
        'unread': cpid,
    })
    
    mydb[ColChallengeDetail].insert_one({
        'homeid': homeid,
        'challenge_id': challenge_id,
        'time': int(time.time()*1000),
        'user_id': open_id,
        'notes': "使用了恋爱兑换券:" + res['title'],
        'pic': "",
        'process': 0
    })
    
    return True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    