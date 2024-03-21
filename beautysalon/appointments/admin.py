from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Salon)
admin.site.register(models.Service)
admin.site.register(models.Employee)
admin.site.register(models.Appointment)
admin.site.register(models.Review)