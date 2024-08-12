from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.contrib import messages
import pandas as pd
from apphealth.models.model_init import DataSetCollection, DataTestingCollection, DataTrainingCollection
from apphealth.decorators import login_required
from bson import ObjectId


collectionDataset = DataSetCollection()
collectionData_Training = DataTrainingCollection()
collectionData_Testing = DataTestingCollection()

@login_required
@require_GET
def index(request):
    dataset = list(collectionDataset.find())
    for item in dataset:
        item['id_str'] = str(item['_id'])
    
    data_training = list(collectionData_Training.find())
    for item in data_training:
        item['id_str'] = str(item['_id'])
        
    data_testing = list(collectionData_Testing.find())
    for item in data_testing:
        item['id_str'] = str(item['_id'])
    
    existing_ids = set(item['_id'] for item in dataset)

    # Menggabungkan data training ke dalam dataset
    for item in data_training:
        if item['_id'] not in existing_ids:
            collectionDataset.insert_one(item)
            existing_ids.add(item['_id'])

    # Menggabungkan data testing ke dalam dataset
    for item in data_testing:
        if item['_id'] not in existing_ids:
            collectionDataset.insert_one(item)
            existing_ids.add(item['_id'])

    return render(request, 'dataset/index.html',{
        'dataset':dataset,  
        'data_testing':data_testing,
        'data_training':data_training,
        
    })
    

def create(request):
    return render(request, 'dataset/create.html')

def edit(request, id):
    dataset = collectionDataset.find_one({'_id': ObjectId(id)})
    if not dataset:
        messages.error(request, 'Dataset tidak ditemukan')
        return redirect('dataset.index')
    blood_pressure=dataset['blood_pressure'].split('/')
    dataset['systolic'] = blood_pressure[0]
    dataset['diastolic'] = blood_pressure[1]
    dataset['id_str'] = str(dataset['_id'])
        

    return render(request, 'dataset/edit.html', {
        'dataset': dataset
    })

def store(request):
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    cholesterol = request.POST.get('cholesterol')
    systolic = request.POST.get('systolic')
    diastolic = request.POST.get('diastolic')
    heartRate = request.POST.get('heartRate')
    bmi = request.POST.get('bmi')
    bmiStatus = request.POST.get('bmiStatus')
    heartRisk = request.POST.get('heart_attack_risk')
    glucose = request.POST.get('glucose')


    newDiabetes = 1 if request.POST.get('diabetes') == 'yes' else 0
    newSmoking = 1 if request.POST.get('smoking') == 'yes' else 0
    obesity = int(request.POST.get('obesity'))
    heartRisk = 'yes' if heartRisk == "1" else 'No'
    
    newData = {
        'age': age,
        'sex': gender.capitalize(),
        'cholesterol': cholesterol,
        'blood_pressure': f'{systolic}/{diastolic}',
        'heart_rate': heartRate,
        'diabetes': newDiabetes,
        'smoking': newSmoking,
        'obesity': obesity,
        'bmi': bmi,
        'glucose': glucose,
        'heart_attack_risk': heartRisk
    }

    collectionDataset.insert_one(newData)
    messages.success(request, 'Dataset berhasil ditambahkan')
    return redirect('dataset.index')

def updated(request, id):
    dataset = collectionDataset.find_one({'_id': ObjectId(id)})
    if not dataset:
        messages.error(request, 'Dataset tidak ditemukan')
        return redirect('dataset.index')

    age = request.POST.get('age')
    gender = request.POST.get('gender')
    cholesterol = request.POST.get('cholesterol')
    systolic = request.POST.get('systolic')
    diastolic = request.POST.get('diastolic')
    heartRate = request.POST.get('heartRate')
    bmi = request.POST.get('bmi')
    bmiStatus = request.POST.get('bmiStatus')
    heartRisk = request.POST.get('heart_attack_risk')
    glucose = request.POST.get('glucose')

    newDiabetes = 1 if request.POST.get('diabetes') == 'yes' else 0
    newSmoking = 1 if request.POST.get('smoking') == 'yes' else 0
    obesity = int(request.POST.get('obesity'))
    heartRisk = 'yes' if heartRisk == "1" else 'No'

    data = {
        'age': age,
        'sex': gender.capitalize(),
        'cholesterol': cholesterol,
        'blood_pressure': f'{systolic}/{diastolic}',
        'heart_rate': heartRate,
        'diabetes': newDiabetes,
        'smoking': newSmoking,
        'obesity': obesity,
        'bmi': bmi,
        'glucose': glucose,
        'heart_attack_risk': heartRisk
    }
    if dataset != data:
        collectionDataset.update_one({'_id': ObjectId(id)}, {'$set': data})
        messages.success(request, 'Dataset berhasil diperbarui')
        return redirect('dataset.index')
    else: 
        return redirect('dataset.index')

def destroy(request, id):
    dataset = collectionDataset.find_one({'_id': ObjectId(id)})
    if not dataset:
        messages.error(request, 'Dataset tidak ditemukan')
        return redirect('dataset.index')
    collectionDataset.delete_one({'_id': ObjectId(id)})
    messages.success(request, 'Dataset berhasil dihapus')
    return redirect('dataset.index')


def importDataExcel(request):
    excel_file = request.FILES['file']

    # Check the file extension
    if not excel_file.name.endswith(('.xls', '.xlsx')):
        messages.error(request, 'Please upload an Excel file (.xls or .xlsx)')
        return redirect('dataset.index')

    # Load the Excel file
    if excel_file.name.endswith('.xlsx'):
        df = pd.read_excel(excel_file, engine='openpyxl')
    else:
        df = pd.read_excel(excel_file, engine='xlrd')

    # Definisikan nama kolom yang diharapkan
    expected_columns = [
        'Gender', 'age', 'Smoker', 'diabetes', 'Chol', 
        'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose','Heart_risk'
    ]

    # # Memastikan header sesuai dengan yang diharapkan
    if list(df.columns) != expected_columns:
        messages.error(request, f"Expected columns: {expected_columns}, but got: {list(df.columns)}")
        return redirect('dataset.index')

    # Process header (example: just show it in messages or further logic)
    datasetManyData = [] 
    for index, row in df.iterrows():
        # Example of processing each row
        row_data = row.to_dict()
        age = row_data['age']
        sex = row_data['Gender']
        cholesterol = row_data['Chol']
        blood_pressure = str(row_data['sysBP']) + '/' + str(row_data['diaBP'])
        heart_rate = row_data['heartRate']
        diabetes = row_data['diabetes']
        smoking = row_data['Smoker']
        glucose = row_data['glucose']
        bmi = row_data['BMI']
        obesity = is_obese(float(row_data['BMI']))
        heart_attack_risk = row_data['Heart_risk']
        
        datasetManyData.append({
            'age': age,
            'sex': sex,
            'cholesterol': cholesterol,
            'blood_pressure': blood_pressure,
            'heart_rate': heart_rate,
            'diabetes': diabetes,
            'smoking': smoking,
            'obesity': obesity,
            'glucose': glucose,
            'bmi': bmi,
            'heart_attack_risk': heart_attack_risk
        })

    # Insert data into the database (replace `collectionDataset` with your actual collection)
    collectionDataset.insert_many(datasetManyData)
    messages.success(request, 'Successfully imported dataset')
    return redirect('dataset.index')
    
def is_obese(bmi):
    if bmi >= 30:
        return 1
    else:
        return 0