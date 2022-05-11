from django.contrib import admin
from general_app.models import *
# Register your models here.

admin.site.register(AuthUser)
admin.site.register(AuthUserGroups)
admin.site.register(Patient)
admin.site.register(Examinations)
admin.site.register(UnacceptedExaminations)
admin.site.register(HospitalStaff)
admin.site.register(Rooms)
admin.site.register(Departments)
admin.site.register(Timetable)