from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewBase.as_view(), name='home'),  # Home"""  """
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/<int:id_recipe>/', views.recipe, name='recipe'),
]
