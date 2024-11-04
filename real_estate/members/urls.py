# members/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, login_view, property_list_view,signup_view, profile_view,logout_view,dashboard_view , agent_login_view , agent_dashboard_view, buy_property_view,sell_property_view,property_detail_view,find_agent_view,property_brochure

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('properties/', property_list_view, name='property_list'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # path('agent-signup/', agent_signup , name = 'agent_signup'),
    path('agent-login/', agent_login_view, name='agent_login'),
    path('agent-dashboard/', agent_dashboard_view, name='agent_dashboard'),
    path('dashboard/buy/', buy_property_view, name='buy'),
    path('agent-dashboard/sell/', sell_property_view, name='sell'),
    path('property/<int:property_id>/', property_detail_view, name='property_detail'),
    path('find-agent/', find_agent_view, name='find_agent'),
    path('property/<int:property_id>/brochure/', property_brochure, name='property_brochure'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)