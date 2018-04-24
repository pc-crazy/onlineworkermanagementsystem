# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from info.models import *
from worker.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number','first_name','last_name','type' ,'is_admin']

admin.site.register(WorkerSkill)
admin.site.register(ContractorProfile)
admin.site.register(WorkerProfile)
admin.site.register(HireWorker)

admin.site.register(User, UserAdmin)