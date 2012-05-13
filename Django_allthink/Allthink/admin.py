from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

__author__ = 'NIENNGUYEN'

from django.contrib import admin
from Allthink.models import *
class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile,UserAdmin)

admin.site.register(Lesson)

admin.site.register(File_doc)
admin.site.register(File_img)
admin.site.register(Document)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Text)
admin.site.register(StepbyStep)

