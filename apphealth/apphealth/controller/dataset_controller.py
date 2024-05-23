from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.contrib import messages
import pandas as pd
from apphealth.models.model_init import DataSetCollection
from apphealth.decorators import login_required
from bson import ObjectId


collectionDataset = DataSetCollection()

@login_required
@require_GET
def index(request):
    dataset = list(collectionDataset.find())
    for item in dataset:
        item['id_str'] = str(item['_id'])
        
    return render(request, 'dataset/index.html',{
        'dataset':dataset
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
    eatingPatterns = request.POST.get('eatingPatterns')
    bmi = request.POST.get('bmi')
    bmiStatus = request.POST.get('bmiStatus')
    heartAttackRisk = request.POST.get('heart_attack_risk')


    newDiabetes = 1 if request.POST.get('diabetes') == 'yes' else 0
    newFamilyHistory = 1 if request.POST.get('familyHistory') == 'yes' else 0
    newSmoking = 1 if request.POST.get('smoking') == 'yes' else 0
    obesity = int(request.POST.get('obesity'))
    newData = {
        'age': age,
        'sex': gender.capitalize(),
        'cholesterol': cholesterol,
        'blood_pressure': f'{systolic}/{diastolic}',
        'heart_rate': heartRate,
        'diabetes': newDiabetes,
        'family_history': newFamilyHistory,
        'smoking': newSmoking,
        'obesity': obesity,
        'diet': eatingPatterns.capitalize(),
        'bmi': bmi,
        'heart_attack_risk': heartAttackRisk
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
    eatingPatterns = request.POST.get('eatingPatterns')
    bmi = request.POST.get('bmi')
    bmiStatus = request.POST.get('bmiStatus')
    heartAttackRisk = request.POST.get('heart_attack_risk')


    newDiabetes = 1 if request.POST.get('diabetes') == 'yes' else 0
    newFamilyHistory = 1 if request.POST.get('familyHistory') == 'yes' else 0
    newSmoking = 1 if request.POST.get('smoking') == 'yes' else 0
    obesity = int(request.POST.get('obesity'))
    data = {
        'age': age,
        'sex': gender.capitalize(),
        'cholesterol': cholesterol,
        'blood_pressure': f'{systolic}/{diastolic}',
        'heart_rate': heartRate,
        'diabetes': newDiabetes,
        'family_history': newFamilyHistory,
        'smoking': newSmoking,
        'obesity': obesity,
        'diet': eatingPatterns.capitalize(),
        'bmi': bmi,
        'heart_attack_risk': heartAttackRisk
    }
    collectionDataset.update_one({'_id': ObjectId(id)}, {'$set': data})
    messages.success(request, 'Dataset berhasil diperbarui')
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
        'Age', 'Sex', 'Cholesterol', 'Blood Pressure', 'Heart Rate', 'Diabetes', 
        'Family History', 'Smoking', 'Obesity', 'Diet', 'BMI', 'Heart Attack Risk'
    ]

    # Memastikan header sesuai dengan yang diharapkan
    if list(df.columns) != expected_columns:
        messages.error(request, f"Expected columns: {expected_columns}, but got: {list(df.columns)}")
        return redirect('dataset.index')

    # Process header (example: just show it in messages or further logic)
    datasetManyData = [] 
    for index, row in df.iterrows():
        # Example of processing each row
        row_data = row.to_dict()
        age = row_data['Age']
        sex = row_data['Sex']
        cholesterol = row_data['Cholesterol']
        blood_pressure = row_data['Blood Pressure']
        heart_rate = row_data['Heart Rate']
        diabetes = row_data['Diabetes']
        family_history = row_data['Family History']
        smoking = row_data['Smoking']
        obesity = row_data['Obesity']
        diet = row_data['Diet']
        bmi = row_data['BMI']
        heart_attack_risk = row_data['Heart Attack Risk']
        
        datasetManyData.append({
            'age': age,
            'sex': sex,
            'cholesterol': cholesterol,
            'blood_pressure': blood_pressure,
            'heart_rate': heart_rate,
            'diabetes': diabetes,
            'family_history': family_history,
            'smoking': smoking,
            'obesity': obesity,
            'diet': diet,
            'bmi': float(bmi),
            'heart_attack_risk': heart_attack_risk
        })

    # Insert data into the database (replace `collectionDataset` with your actual collection)
    collectionDataset.insert_many(datasetManyData)
    messages.success(request, 'Successfully imported dataset')
    return redirect('dataset.index')
    
