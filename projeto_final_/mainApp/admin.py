from django.contrib import admin
import mainApp
from django.apps import apps

models = apps.get_models()
filteredModels = []

for model in models:
    if model._meta.app_label == "mainApp":
        filteredModels.append(model)

for model in filteredModels:
    admin.site.register(model)


# Register your models here.
