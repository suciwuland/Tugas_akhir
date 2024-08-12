"""
URL configuration for apphealth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apphealth.controller import dataset_controller,pasien_controller,general_controller

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("",general_controller.index,name="index-klasifikasi"),
    path('hasil-klasifikasi-pasien/<str:id>',general_controller.resultKlasifikasi,name="klasifikasi.result.pasien"),
    path('input-klasifikasi',general_controller.clasificationView,name="klasifikasi.index"),
    path('hasil-klasifikasi',general_controller.clasificationInsert,name="klasifikasi.result"),
    path('unduh-pdf/<str:id>/', general_controller.generate_pdf, name='generate_pdf'),
    path('report-klasifikasi-pasien/<str:id>',general_controller.reportKlasifikasi,name="report_klasifikasi_page"),
    
    path('data-set',dataset_controller.index,name="dataset.index"),
    path('data-set/import',dataset_controller.importDataExcel,name="dataset.importexcel"),
    path('data-set/create',dataset_controller.create,name="dataset.create"),
    path('data-set/store',dataset_controller.store,name="dataset.store"),
    path('data-set/edit/<str:id>/',dataset_controller.edit,name="dataset.edit"),
    path('data-set/update/<str:id>/',dataset_controller.updated,name="dataset.update"),
    path('data-set/delete/<str:id>',dataset_controller.destroy,name="dataset.destroy"),
    


    path('data-pasien',pasien_controller.index,name="pasien.index"),
    path('data-pasien/laporan', pasien_controller.laporan, name='laporan_pdf'),
    path('report-pasien', pasien_controller.report_pasien, name='laporan_pasien'),
    path('data-pasien/delete/<str:id>/',pasien_controller.destroy, name="pasien.destroy"),
    path('login/', general_controller.login_view, name='login'),
    path('auth/', general_controller.auth, name='login.auth'),
    path('logout/', general_controller.logout_view, name='logout'),
    path('register/', general_controller.signup_view, name='register'),
    path('register/store', general_controller.storeRegister, name='register.store'),
    path('admin/approval/', general_controller.list_users_for_approval, name='list_users_for_approval'),
    path('admin-approval/', general_controller.admin_approval, name='admin.approval'),
    path('admin/approve/<str:user_id>/', general_controller.approve_user_view, name='approve_user'),
    path('reject_user/<str:user_id>/', general_controller.reject_user, name='reject_user'),
]
