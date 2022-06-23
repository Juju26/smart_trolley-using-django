from django import views
from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('',csrf_exempt(views.login),name="Login"),
    path('Register',csrf_exempt(views.register), name="Register"),
    path('Admin',views.admin, name="Admin"),
    path('home',views.home, name="home"),
    path('add_product',views.add_product,name='add_product'),
    path('set_location_product',views.set_location_product,name='set_location_product'),
    path('upload_image',views.upload_image,name='upload_image'),
    path('view_layout',views.view_layout,name='view_layout'),
    path('view_mapped_layout',views.view_mapped_layout,name='view_mapped_layout'),
    path('tables',views.tables,name='tables'),
    path('CustomerHome',views.CustomerHome,name="CustomerHome"),
    path('cart',views.cart,name="cart"),
    # path('login',views.login,name='login'),
    # path('register',views.register,name='register'),
    path('settings',views.settings,name='settings'),
    path('loading',views.loading,name='loading'),
    path('404',views.error_404,name='404'),
]