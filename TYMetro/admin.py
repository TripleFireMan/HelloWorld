from django.contrib import admin
from TYMetro.models import UserProfile
from TYMetro.models import FeedBack
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    exclude = ('date_joined','first_name','last_name','is_staff','is_active','last_login','is_superuser','groups','user_permissions')
    list_display = ('username','nick_name',"birthday","gender","address","mobile","introduce","email","img","third_source","apple_id")
    fieldsets = (
        ('基本信息',{'fields':('username',('nick_name','birthday',"gender",),'introduce','img',"address",)}),
        ('联系方式',{'fields':("mobile",'email')}),
        ('其他',{'fields':("third_source","apple_id")}),
    )

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(FeedBack)