from django.contrib import admin
from web.models import *
from django.apps import apps

class RaceResultAdmin(admin.ModelAdmin):
  readonly_fields = ('DriverResults',)

class DriverResultAdmin(admin.ModelAdmin):
  exclude = ('Laps',)


for model in apps.get_app_config('web').models.values():
  if "_" not in str(model) and "Lap" not in str(model):
    if "RaceResult" not in str(model) and "DriverResult" not in str(model):
      admin.site.register(model)

admin.site.register(RaceResult, RaceResultAdmin)
admin.site.register(DriverResult, DriverResultAdmin)