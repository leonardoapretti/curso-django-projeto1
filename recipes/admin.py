from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    ...


class RecipeAdmin(admin.ModelAdmin):
    ...


admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Category, CategoryAdmin)
