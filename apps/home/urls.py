from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login_page/', views.login_page, name="login_page"),
    path('register_page/', views.register_page, name="register_page"),
    path('signout/', views.signout, name="signout"),
    path('make_login_default/', views.make_login_default, name="make_login_default"),
    path('make_register_default/', views.make_register_default, name="make_register_default"),
]