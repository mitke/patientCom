from django.contrib import admin
from .models import Patient, Contact

class PatientAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'jmbg')


admin.site.register(Patient)
admin.site.register(Contact)
