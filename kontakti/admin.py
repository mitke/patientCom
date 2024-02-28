from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Patient, Contact, OU, UserProfile


class PatientAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'jmbg')


class UserProfileInline(admin.StackedInline):
  model = UserProfile
  can_delete = False


class UserAdmin(BaseUserAdmin):
  inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Patient)
admin.site.register(Contact)
admin.site.register(OU)
