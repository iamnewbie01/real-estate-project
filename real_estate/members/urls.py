# members/urls.py
from django.urls import path
from .views import home_view, login_view, property_list_view,signup_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('properties/', property_list_view, name='property_list'),
]
