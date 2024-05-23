from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET,require_POST
from django.http import HttpResponse
from apphealth.svm.svm import clasificationPredict
from apphealth.models.model_init import DataPasienCollection,DataUserAdmin
from django.contrib import messages
from django.urls import reverse
from bson import ObjectId
from django.contrib.auth.hashers import check_password
collectionDatapasien = DataPasienCollection()
collectionAdmin = DataUserAdmin()


@require_GET
def index(request):
    return render(request, 'index.html')

@require_GET
def clasificationView(request):
    return render(request, 'clasification.html')

@require_POST
def clasificationInsert(request):
   
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    cholesterol = request.POST.get('cholesterol')
    systolic = request.POST.get('systolic')
    diastolic = request.POST.get('diastolic')
    heartRate = request.POST.get('heartRate')
    diabetes = request.POST.get('diabetes')
    familyHistory = request.POST.get('familyHistory')
    smoking = request.POST.get('smoking')
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    eatingPatterns = request.POST.get('eatingPatterns')
    bmi = request.POST.get('bmi')
    bmiStatus = request.POST.get('bmiStatus')
   
    newDiabetes = 1 if request.POST.get('diabetes') == 'yes' else 0
    newFamilyHistory = 1 if request.POST.get('familyHistory') == 'yes' else 0
    newSmoking = 1 if request.POST.get('smoking') == 'yes' else 0
    obesity = 1 if bmiStatus == 'Obesity' else 0
    newData = {
        'Age': [int(age)],
        'Sex': [gender.capitalize()],
        'Cholesterol': [int(cholesterol)],
        'Blood Pressure': [f'{systolic}/{diastolic}'],
        'Heart Rate': [int(heartRate)],
        'Diabetes': [newDiabetes],
        'Family History': [newFamilyHistory],
        'Smoking': [newSmoking],
        'Obesity': [obesity],
        'Diet': [eatingPatterns.capitalize()],
        'BMI': [int(bmi)]
    }
    predict=clasificationPredict(newData)
    stringPredict = 'Risk' if predict == 1 else "No Risk"

    dataPasien = {
        'age': age,
        'gender': gender.capitalize(),
        'cholesterol': cholesterol,
        'systolic': systolic,
        'diastolic': diastolic,
        'heartRate': heartRate,
        'diabetes': diabetes,
        'familyHistory': familyHistory.capitalize(),
        'smoking': smoking.capitalize(),
        'height': height,
        'weight': weight,
        'bmi': bmi,
        'bmiStatus': bmiStatus,
        'eatingPatterns': eatingPatterns.capitalize(),
        "prediction":stringPredict 
    }

    insertPasien=collectionDatapasien.insert_one(dataPasien)
    return redirect(reverse('klasifikasi.result.pasien', args=[insertPasien.inserted_id]))

def resultKlasifikasi(request,id):
    dataPasien = collectionDatapasien.find_one({"_id": ObjectId(id)})
    if not dataPasien:
        messages.error(request, 'Data tidak ditemukan')
        return redirect('klasifikasi.index')
    return render(request, 'result.html',dataPasien)


def login_view(request):
    return render(request, 'login.html')

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = collectionAdmin.find_one({"username":username})
    if user:
        if check_password(password,user['password']):
            request.session['user_id'] = str(user['_id'])  # Simpan ID pengguna dalam sesi
            messages.success(request, "Login berhasil!")
            return redirect('dataset.index')
        else:
            messages.error(request,"password tidak valid")
            return redirect('login')
    else:
        messages.error(request,"username tidak valid")
        return redirect('login')   
    
    

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "Logout berhasil!")
    return redirect('login')

def signup_view(request):
    # Implement signup logic here
    return render(request, 'accounts/signup.html')