# members/urls.py
from django.urls import path
from .views import home_view, login_view, property_list_view,signup_view, profile_view,logout_view,dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('properties/', property_list_view, name='property_list'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
