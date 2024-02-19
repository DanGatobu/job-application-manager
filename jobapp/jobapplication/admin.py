from django.contrib import admin

# Register your models here.
# copilot register all models
from .models import resumetemplates,coverletter,mergeddocs,cv,email,created_resumes,created_coverletters,sent_application

admin.site.register(resumetemplates)
admin.site.register(coverletter)
admin.site.register(mergeddocs)
admin.site.register(cv)
admin.site.register(email)
admin.site.register(created_resumes)
admin.site.register(created_coverletters)
admin.site.register(sent_application)
