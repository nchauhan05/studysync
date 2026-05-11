
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.welcome),
    path('login/', views.login_view, name='login'),
    path('register/', views.register),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('logout/', views.logout_view, name='logout'),
]