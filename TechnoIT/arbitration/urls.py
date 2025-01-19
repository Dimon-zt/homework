from django.urls import path
from . import views

urlpatterns = [
    path('', views.arbitration, name='arbitration'),
    path('arbitration/', views.arbitration, name='arbitration'),
    path('add_exchange/', views.add_exchange, name='add_exchange'),
    path('set_interval/', views.set_interval, name='set_interval'),
]

