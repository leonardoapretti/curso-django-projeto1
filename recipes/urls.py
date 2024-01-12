from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.home, name='home'),  # Home
    path('recipes/<int:id>/', views.recipe, name='recipe'),
]
