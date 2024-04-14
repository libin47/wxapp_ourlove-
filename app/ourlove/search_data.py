from database import mydb
import pymongo

def fun_find_data(arg):
    # print(arg)
    dbname = arg['dbname']
    data = arg['data']
    result = mydb[dbname].find(data)
    if 'sortdata' in arg.keys():
        sortdata = arg['sortdata']
        for key in sortdata.keys():
            if sortdata[key]=='desc':
                result.sort(key, pymongo.DESCENDING)
            else:
                result.sort(key, pymongo.ASCENDING)
    return list(result)
