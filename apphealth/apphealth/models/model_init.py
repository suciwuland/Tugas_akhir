from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
db = client['db_jantung']

def DataPasienCollection():
    return db['datapasien']

def DataSetCollection():
    return db['dataset']

def DataTrainingCollection():
    return db['data_training']

def DataTestingCollection():
    return db['data_testing']

def DataUserAdmin():
    return db['user_admin']

def dataPasienBar():
    data = {}
    data['labels'] = ["0", "1"]  # 0 untuk No risk, 1 untuk Risk
    data["male"] = [0, 0]
    data["female"] = [0, 0]
    collection = DataPasienCollection().find()
    for i in collection:
        if i['gender'] == "Male":
            if i['prediction'] == 'Risk':
                data["male"][1] += 1  # Menambahkan ke indeks 1
            else:
                data["male"][0] += 1  # Menambahkan ke indeks 0
        else:
            if i['prediction'] == 'Risk':
                data["female"][1] += 1  # Menambahkan ke indeks 1
            else:
                data["female"][0] += 1  # Menambahkan ke indeks 0
    return data


def dataPasienPie():
    data = {}
    data['labels'] = ['Yes', 'No']
    data["data"] = [0, 0]
    collection = DataPasienCollection().find()
    for i in collection:
        if i['smoking'] == 'Yes':
            data["data"][0] += 1  # Menambahkan jumlah perokok ke indeks 0
        else:
            data["data"][1] += 1  # Menambahkan jumlah bukan perokok ke indeks 1
    return data
    
