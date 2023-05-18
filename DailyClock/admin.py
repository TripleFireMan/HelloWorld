from django.contrib import admin
from DailyClock.models import DKFeedBack,DKJiTang,DKVersionHistory
# Register your models here.

class DKFeedBackAdmin(admin.ModelAdmin):
    list_display = ('title','content','phone','date','reply')

class DKJitangAdmin(admin.ModelAdmin):
    list_display = ('text','url','date','wordsInfo')

class DKVersionHistoryAdmin(admin.ModelAdmin):
    list_display = ('version','des')

admin.site.register(DKFeedBack, DKFeedBackAdmin)
admin.site.register(DKVersionHistory,DKVersionHistoryAdmin)
admin.site.register(DKJiTang,DKJitangAdmin)