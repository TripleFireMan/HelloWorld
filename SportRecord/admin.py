from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.
class SRUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SRUserProfile._meta.get_fields() if field not in ['partner_id']]
class SRCategroyAdmin(admin.ModelAdmin):
    list_display = ['name','icon']
class SRRecordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SRUserSportRecord._meta.get_fields()]
class SRPartnerAdmin(admin.ModelAdmin):
    def avator_tag(self, obj):
        if (obj.avator):
            return format_html('<img src="https://triplefireman.com/media/{}" style="height:25px;width:25px">'.format(obj.avator))
    list_display = ['id','name','avator_tag','gender','mobile','birthday','remark']
class SRPropertyAdmin(admin.ModelAdmin):
    list_display = ['name','icon']
class SRSystemConfigAdmin(admin.ModelAdmin):
    list_display = ['name','isInAppStoreView']
admin.site.register(SRUserProfile,SRUserAdmin)
admin.site.register(SRSportCategory,SRCategroyAdmin)
admin.site.register(SRUserSportRecord,SRRecordAdmin)
admin.site.register(SRPartner,SRPartnerAdmin)
admin.site.register(SRProperty,SRPropertyAdmin)
admin.site.register(SRSystemConfig,SRSystemConfigAdmin)