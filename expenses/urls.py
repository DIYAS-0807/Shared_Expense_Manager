from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('members/', views.members, name='members'),
    path('balance/', views.balance, name='balance'),
]
