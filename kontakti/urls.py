from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.user_logout, name='logout'),
    path('add_patient/', views.add_patient, name='add_patient'),  
    path('patient/<int:patient_id>', views.patient, name='patient'),
    path('add_contact/<int:pk>', views.add_contact, name='add_contact'),
    path('edit_patient/<int:patient_id>', views.edit_patient, name='edit_patient'),
]
