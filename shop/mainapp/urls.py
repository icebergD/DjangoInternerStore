from django.urls import path
from . import views

urlpatterns = [
    path('hell/', views.hello),
]
