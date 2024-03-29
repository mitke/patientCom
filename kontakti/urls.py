from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reserved', views.reserved, name='reserved'),
    path('next', views.nextWeek, name='next'),
    path('login', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_patient/', views.add_patient, name='add_patient'),  
    path('patient/<int:patient_id>', views.patient, name='patient'),
    path('edit_patient/<int:patient_id>', views.edit_patient, name='edit_patient'),    
    path('delete_patient/<int:patient_id>', views.delete_patient, name='delete_patient'),
    path('add_contact/<int:patient_id>', views.add_contact, name='add_contact'),
    path('edit_contact/<int:patient_id>/<int:contact_id>', views.edit_contact, name='edit_contact'),
    path('search', views.search_patient, name='search'),
]
