from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


admin.site.register(models.Category, CategoryAdmin)
