from django.contrib import admin

from .models import UserDetailInfo


# Register your models here.
@admin.register(UserDetailInfo)
class UserDetailInfoAdmin(admin.ModelAdmin):
    pass
