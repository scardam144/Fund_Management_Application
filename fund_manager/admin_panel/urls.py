from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # Protected dashboard
    path('login/', LoginView.as_view(template_name='admin_panel/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add_stock/', views.add_stock, name='add_stock'),
]
