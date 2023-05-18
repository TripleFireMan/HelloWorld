from django.contrib import admin
from TYMetro.models import UserProfile
from TYMetro.models import FeedBack
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nick_name',"birthday","gender","address","mobile","introduce","email","img","third_source","apple_id")


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(FeedBack)