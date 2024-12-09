from django.contrib import admin
from .models import Participant, Criterios, Scores, CustomUser

# Register your models here.
admin.site.register(Participant)
admin.site.register(Criterios)
admin.site.register(Scores)
admin.site.register(CustomUser)