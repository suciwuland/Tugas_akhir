from django.shortcuts import render, redirect
from bson import ObjectId
from django.contrib import messages
from django.views.decorators.http import require_GET
from apphealth.models.model_init import DataPasienCollection,dataPasienBar,dataPasienPie
from apphealth.decorators import login_required
from django.template.loader import render_to_string
import time
collectionDatapasien = DataPasienCollection()

@login_required
@require_GET
def index(request):
    datapasien = list(collectionDatapasien.find())  
    for item in datapasien:
        item['id_str'] = str(item['_id'])
        
    return render(request, 'pasien/index.html', {"bar_pasien": dataPasienBar(), "pie_pasien": dataPasienPie(), "datapasien": datapasien})

def report_pasien(request):
    datapasien = list(collectionDatapasien.find())  
    for item in datapasien:
        item['id_str'] = str(item['_id'])
    context = {
        'datapasien': datapasien
    }
    return render(request, 'pasien/report.html', context)


def destroy(request, id):
    dataset = collectionDatapasien.find_one({'_id': ObjectId(id)})
    if not dataset:
        messages.error(request, 'Data Pasien tidak ditemukan')
        return redirect('datapasien.index')
    collectionDatapasien.delete_one({'_id': ObjectId(id)})
    messages.success(request, 'Data Pasien berhasil dihapus')
    return redirect('pasien.index')

from django.http import HttpResponse
from weasyprint import HTML

def laporan(request):
    datapasien = list(collectionDatapasien.find())
    for item in datapasien:
        item['id_str'] = str(item['_id'])
    
    context = {
        'datapasien': datapasien
    }
    try:
        html_content = render_to_string('pasien/report.html', context)
        pdf_file = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="laporan_data_pasien_{int(time.time())}.pdf"'
        # Add cache-control headers
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    except Exception as e:
        # Handle exceptions and provide feedback
        return HttpResponse(f"An error occurred: {str(e)}", status=500)