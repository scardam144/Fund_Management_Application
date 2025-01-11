from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/<int:client_id>/invest/', views.invest, name='invest'),
]
