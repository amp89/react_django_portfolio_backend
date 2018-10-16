from django.contrib import admin

# Register your models here.

from restapi.models import SiteInfo
from restapi.models import ContactInfo
from restapi.models import Technology
from restapi.models import Project

from restapi.models import Message


admin.site.register(SiteInfo, admin.ModelAdmin)
admin.site.register(ContactInfo, admin.ModelAdmin)
admin.site.register(Technology, admin.ModelAdmin)
admin.site.register(Project, admin.ModelAdmin)

admin.site.register(Message, admin.ModelAdmin)