from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET,require_POST
from django.http import HttpResponse
from apphealth.svm.svm import clasificationPredict
from apphealth.models.model_init import DataPasienCollection,DataUserAdmin
from django.contrib import messages
from django.urls import reverse
from bson import ObjectId
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password,make_password
from django.template.loader import render_to_string
import requests
import json

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
    smoking = request.POST.get('smoking')
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    glucose = request.POST.get('glucose')
    bmi = request.POST.get('bmi')
    bmiStatus = request.POST.get('bmiStatus')
   
    newDiabetes = 1 if request.POST.get('diabetes') == 'yes' else 0 
    newSmoking = 1 if request.POST.get('smoking') == 'yes' else 0
    obesity = 1 if bmiStatus == 'Obesity' else 0
    newData = {
        'Age': [int(age)],
        'Sex': [gender.capitalize()],
        'Cholesterol': [int(cholesterol)],
        'Blood Pressure': [f'{systolic}/{diastolic}'],
        'Heart Rate': [int(heartRate)],
        'Diabetes': [newDiabetes],
        'Smoking': [newSmoking],
        'Obesity': [obesity],
        'Glucose': [glucose],
        'BMI': [bmi]
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
        'smoking': smoking.capitalize(),
        'height': height,
        'glucose':glucose,
        'weight': weight,
        'bmi': bmi,
        'bmiStatus': bmiStatus,
        'prediction':stringPredict,
    }

    insertPasien=collectionDatapasien.insert_one(dataPasien)
    return redirect(reverse('klasifikasi.result.pasien', args=[insertPasien.inserted_id]))


def resultKlasifikasi(request,id):
    dataPasien = collectionDatapasien.find_one({"_id": ObjectId(id)})
    if not dataPasien:
        messages.error(request, 'Data tidak ditemukan')
        return redirect('klasifikasi.index')
    context = {
        'id': id,
        'age': dataPasien.get('age'),
        'gender': dataPasien.get('gender'),
        'cholesterol': dataPasien.get('cholesterol'),
        'systolic': dataPasien.get('systolic'),
        'diastolic': dataPasien.get('diastolic'),
        'heartRate': dataPasien.get('heartRate'),
        'glucose': dataPasien.get('glucose'),
        'smoking': dataPasien.get('smoking'),
        'bmi': dataPasien.get('bmi'),
        'bmiStatus': dataPasien.get('bmiStatus'),
        'prediction': dataPasien.get('prediction'),
    }
    return render(request,'result.html',context)

    
def reportKlasifikasi(request,id):
    dataPasien = collectionDatapasien.find_one({"_id": ObjectId(id)})
    if not dataPasien:
        messages.error(request, 'Data tidak ditemukan')
        return redirect('klasifikasi.index')
    context = {
        'id': id,
        'age': dataPasien.get('age'),
        'gender': dataPasien.get('gender'),
        'cholesterol': dataPasien.get('cholesterol'),
        'systolic': dataPasien.get('systolic'),
        'diastolic': dataPasien.get('diastolic'),
        'heartRate': dataPasien.get('heartRate'),
        'glucose': dataPasien.get('glucose'),
        'smoking': dataPasien.get('smoking'),
        'bmi': dataPasien.get('bmi'),
        'bmiStatus': dataPasien.get('bmiStatus'),
        'prediction': dataPasien.get('prediction'),
    }
    return render(request,'report.html',context)


def login_view(request):
    return render(request, 'login.html')

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = collectionAdmin.find_one({"username": username})
    
    if user:
        if not user.get('is_approved'):
            messages.error(request, "Akun Anda belum di-approve oleh admin.")
            return redirect('login')
        
        if check_password(password, user['password']):
            request.session['user_id'] = str(user['_id'])  # Simpan ID pengguna dalam sesi
            messages.success(request, "Login berhasil!")
            return redirect('pasien.index')
        else:
            messages.error(request, "Password tidak valid.")
            return redirect('login')
    else:
        messages.error(request, "Username tidak valid.")
        return redirect('login')

    
def admin_approval(request):
    # Asumsikan kamu menggunakan MongoDB dan collectionAdmin
    pending_users = collectionAdmin.find({"is_approved": False})
    
    # Buat list baru dengan mengganti _id menjadi id
    users_with_id = []
    for user in pending_users:
        user['id'] = str(user['_id'])
        users_with_id.append(user)
    return render(request, 'admin_approval.html', {'pending_users': users_with_id})

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "Logout berhasil!")
    return redirect('login')

def signup_view(request):   
    return render(request, 'register.html')

def get_metadata_from_urls(url_list):
    metadata_list = []
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        meta_description = soup.find('meta', attrs={'name': 'description'})
        description = meta_description['content'] if meta_description else ''
        meta_image = soup.find('meta', attrs={'property': 'og:image'})
        image = meta_image['content'] if meta_image else ''
        metadata = {
            'title': title,
            'description': description,
            'image': image,
            'url': url
        }
        metadata_list.append(metadata)
    return json.dumps(metadata_list, indent=2)

def create_user(data):
    data['is_approved'] = False  # Default is False saat user register
    return DataUserAdmin().insert_one(data)

def approve_user(user_id):
    return DataUserAdmin().update_one({"_id": ObjectId(user_id)}, {"$set": {"is_approved": True}})


def list_users_for_approval(request):
    # Mengambil semua pengguna admin yang belum disetujui
    pending_users = list(collectionAdmin.find({'is_approved': False}))
    
    # Mengubah _id menjadi id untuk keperluan tampilan
    for user in pending_users:
        user['id_str'] = str(user['_id'])

    return render(request, 'admin_approval.html', {
        'pending_users': pending_users
    })
    
def approve_user_view(request, user_id):
        approve_user(user_id)
        messages.success(request, "User berhasil di-approve.")
        return redirect('list_users_for_approval')

def reject_user(request, user_id):
    try:
        # Mendapatkan pengguna berdasarkan ID dari MongoDB
        user = collectionAdmin.find_one({'_id': ObjectId(user_id)})
        
        if user is None:
            # Jika pengguna tidak ditemukan, tampilkan pesan kesalahan dan redirect
            messages.error(request, "Pengguna tidak ditemukan.")
            return redirect('list_users_for_approval')
        
        # Simpan nama pengguna untuk pesan sukses
        username = user.get('username', 'Tidak Diketahui')  # Ganti 'username' jika nama field berbeda
        
        # Simpan perubahan
        collectionAdmin.update_one({'_id': ObjectId(user_id)}, {'$set': user})
        
        # Hapus pengguna dari collectionAdmin
        collectionAdmin.delete_one({'_id': ObjectId(user_id)})
        
        # Tambahkan pesan sukses dengan username
        messages.success(request, f'Pengguna dengan username {username} telah ditolak dan dihapus.')
        
    except Exception as e:
        # Tangani kesalahan jika ada masalah saat mengakses MongoDB
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
    
    # Redirect kembali ke halaman daftar pengguna untuk persetujuan
    return redirect('list_users_for_approval')

def storeRegister(request):
    form = request.POST

    if form['password'] != form['password_confirm']:
        messages.error(request, "Password tidak sama")
        return redirect('register')

    data = {
        'nama_user': form['nama_user'],
        'username': form['username'],
        'password': make_password(form['password']),
        'is_approved': False,
    }
    
    existing_user = collectionAdmin.find_one({'username': data['username']})
    if existing_user:
        messages.error(request, 'Username sudah terdaftar')
        return redirect('register')
    
    collectionAdmin.insert_one(data)
    messages.success(request, 'User berhasil ditambahkan')
    
    return redirect('login')

from django.http import HttpResponse
from weasyprint import HTML

def generate_pdf(request, id):
    try:
        # Konversi id ke ObjectId
        object_id = ObjectId(id)
    except Exception as e:
        # Tangani kasus ketika id tidak valid
        messages.error(request, 'ID tidak valid.')
        return redirect('klasifikasi.index')

    # Ambil data pasien berdasarkan id
    dataPasien = collectionDatapasien.find_one({"_id": object_id})
    if not dataPasien:
        messages.error(request, 'Data tidak ditemukan')
        return redirect('klasifikasi.index')
    dataPasien['id_str'] = str(dataPasien['_id'])
    context = {
        'id': id,
        'age': dataPasien.get('age'),
        'gender': dataPasien.get('gender'),
        'cholesterol': dataPasien.get('cholesterol'),
        'systolic': dataPasien.get('systolic'),
        'diastolic': dataPasien.get('diastolic'),
        'heartRate': dataPasien.get('heartRate'),
        'glucose': dataPasien.get('glucose'),
        'smoking': dataPasien.get('smoking'),
        'bmi': dataPasien.get('bmi'),
        'bmiStatus': dataPasien.get('bmiStatus'),
        'prediction': dataPasien.get('prediction'),
    }
    html_content = render_to_string('report.html',context)
    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report_pasien.pdf"'
    return response