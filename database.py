import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["wxapp"]

ColChallenge = "challenge"
ColChallengeDemo = "challenge_demo"
ColChallengeDetail = "challenge_detail"
ColChallengeWait = "challenge_wait"
ColHome = "home"
ColHomeMembers = "home_members"
ColMoonDead = "moon_dead"
ColNotebook = "notebook"
ColPoints = "points"
ColReward = "reward"
ColUser = "user"


dicedb = myclient["COC"]
ColGame = "COC"
ColGroup = "group"
ColUser = "user"
ColPc = "pc_card"