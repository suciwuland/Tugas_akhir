from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client['db_jantung']

def DataPasienCollection():
    return db['datapasien']

def DataSetCollection():
    return db['dataset']

def DataUserAdmin():
    return db['user_admin']

def dataPasienBar():
    data={};
    data['labels']=["0","1"]
    data["male"]=[0,0]
    data["female"]=[0,0]
    collection=DataPasienCollection().find()
    for i in collection:
        if i['gender']=="Male":
            if i['prediction'] == 'No risk':
                data["male"][0]+=1
            else:
                data["male"][1]+=1
        else:
            if i['prediction'] == 'No risk':
                data["female"][0]+=1
            else:
                data["female"][1]+=1
    return data


def dataPasienPie():
    data={};
    data['labels']=['Average', 'Unhealthy', 'Healthy']
    data["data"]=[0,0,0]
    collection=DataPasienCollection().find()
    for i in collection:
        if  i['eatingPatterns'] == 'Average':
            data["data"][0]+=1
        elif i['eatingPatterns'] == 'Unhealthy':
            data["data"][1]+=1
        else:
            data["data"][2]+=1
    return data