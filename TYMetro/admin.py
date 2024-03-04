from django.contrib import admin
from TYMetro.models import UserProfile
from TYMetro.models import FeedBack
from django.utils.html import format_html
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        if(obj.img):
            return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.img))
        return ""
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'
    exclude = ('date_joined','first_name','last_name','is_staff','is_active','last_login','is_superuser')
    list_display = ('username','nick_name',"birthday","gender","address","mobile","introduce","email","image_tag","third_source","apple_id")
    fieldsets = (
        ('基本信息',{'fields':('username',('nick_name','birthday',"gender",),'introduce','img',"address",)}),
        ('联系方式',{'fields':("mobile",'email')}),
        ('其他',{'fields':("third_source","apple_id")}),
    )

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(FeedBack)