from django.contrib import admin
from DailyClock.models import DKFeedBack,DKJiTang,DKVersionHistory,DKFonts
from django.utils.html import format_html

# Register your models here.

class DKFeedBackAdmin(admin.ModelAdmin):
    list_display = ('title','content','phone','date','reply')

class DKJitangAdmin(admin.ModelAdmin):
    def image_tag(self,obj):
        if(obj.url):
            return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.url))
        return ""
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'
    list_display = ('image_tag','text','date','wordsInfo',)
    fieldsets = ((None,{'fields':('text','wordsInfo','date','url')}),)

class DKVersionHistoryAdmin(admin.ModelAdmin):
    list_display = ('version','des')

class DKFontAdmin(admin.ModelAdmin):
    def file_url(self,obj):
        try:
            if (obj.file.url):
                return obj.file.url
        except Exception as e:
            return ''

    list_display = ('name','font_name','font_bold_name','url','file_url')

admin.site.register(DKFeedBack, DKFeedBackAdmin)
admin.site.register(DKVersionHistory,DKVersionHistoryAdmin)
admin.site.register(DKJiTang,DKJitangAdmin)
admin.site.register(DKFonts, DKFontAdmin)