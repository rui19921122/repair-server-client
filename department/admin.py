from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


