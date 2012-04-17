from django.contrib import admin
from  models import *

class QuestAdmin(admin.ModelAdmin):
    pass

admin.site.register(SubjectChoice, QuestAdmin)
admin.site.register(GradeChoice, QuestAdmin)
admin.site.register(InitValue, QuestAdmin)