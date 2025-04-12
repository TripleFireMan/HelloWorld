from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.

class iconNameBaseAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        if(obj.icon):
            return format_html('<img src="https://triplefireman.com/media/{}" style="width:100px;height:80px;"/>'.format(obj.icon))
    list_display = ['image_tag','name']

@admin.register(SRUserProfile)
class SRUserAdmin(admin.ModelAdmin):
    list_display = ['username','password','mobile','name','avator','address','birthday','created','updated']

@admin.register(SRSportCategory)
class SRCategroyAdmin(iconNameBaseAdmin):
    pass

@admin.register(SRRole)
class SRRoleAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SRMenu)
class SRMenuAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SRUserSportRecord)
class SRRecordAdmin(admin.ModelAdmin):
    list_display = ['id' ,'name','address','measure','duration','isSender','highTime','highTimePartner','shootPlace','isHigh','score','mood','remark']
    fieldsets = (
        ("基础信息", {
            "fields": (
                'name',
                'address',
                "duration",
                "measure",
                'partner',
                'isSender',
                
            ),
        }),
        ("道具与服装", {
            "fields": (
                ('clothings',
                'propertys',),
            ),
        }),
        ("高潮信息", {
            "fields": (
                (
                    'highTime',
                    'highTimePartner',
                    "shootPlace",
                    "isHigh",
                ),
            ),
        }),
        ("评分与情绪", {
            "fields": (
                ('score',
                'mood',),
                'remark',
            ),
        }),
        (None,{
            'fields':('photos',),
        }),
    )
    
    raw_id_fields = ('partner',)

@admin.register(SRPartner)
class SRPartnerAdmin(admin.ModelAdmin):
    def avator_tag(self, obj):
        if (obj.avator):
            return format_html('<img src="https://triplefireman.com/media/{}" style="height:25px;width:25px">'.format(obj.avator))
    list_display = ['id','name','avator_tag','gender','mobile','birthday','remark']
    search_fields = ('name','mobile',)

@admin.register(SRProperty)
class SRPropertyAdmin(iconNameBaseAdmin):
    list_display = ['id','name','image_tag','bgColor']

@admin.register(SRSystemConfig)
class SRSystemConfigAdmin(admin.ModelAdmin):
    list_display = ['name','isInReView']
    
@admin.register(SRScore)
class SRScoreAdmin(iconNameBaseAdmin):
    list_display = ['id','name', 'score','image_tag']

@admin.register(SRMood)
class SRMoodAdmin(iconNameBaseAdmin):
    pass

@admin.register(SRClothing)
class SRClothingAdmin(iconNameBaseAdmin):
    list_display = ['id', 'name','image_tag']
    pass

@admin.register(SRPhoto)
class SRPhotoAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        if(obj.url):
            return format_html('<img src="https://triplefireman.com/media/{}" style="width:100px;height:80px;"/>'.format(obj.url))
        return ""
    list_display = ['image_tag','url']
    fieldsets = (
        (None, {
            "fields": (
                'url',
            ),
        }),
    )
    