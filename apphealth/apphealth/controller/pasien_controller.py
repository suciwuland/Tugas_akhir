from django.shortcuts import render
from django.views.decorators.http import require_GET
from apphealth.models.model_init import DataPasienCollection,dataPasienBar,dataPasienPie
from apphealth.decorators import login_required
collectionDatapasien = DataPasienCollection()

@login_required
@require_GET
def index(request):
    datapasien = collectionDatapasien.find()
    return render(request, 'pasien/index.html',{"bar_pasien":dataPasienBar(),'pie_pasien':dataPasienPie(),'datapasien':datapasien})

