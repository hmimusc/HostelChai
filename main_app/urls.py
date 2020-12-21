from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('setup_admin_page/', views.setup_admin_page, name='setup_admin_page'),
    # path('setup_admin/', views.setup_admin, name='setup_admin'),
    path('requests_loader_page/', views.requests_loader_page, name='requests_loader_page'),
    path('requests_loader/', views.requests_loader, name='requests_loader'),
    path('hostel_loader_page/', views.hostel_loader_page, name='hostel_loader_page'),
    path('approve_hostel/', views.approve_hostel, name='approve_hostel'),
    path('login_page/', views.login_page, name='login_page'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home_page/', views.home_page, name='home_page'),
    path('admin_home_page/', views.admin_home_page, name='admin_home_page'),
    path('student_home_page/', views.student_home_page, name='student_home_page'),
    path('hostel_owner_home_page/', views.hostel_owner_home_page, name='hostel_owner_home_page'),
    path('add_hostel_page/', views.add_hostel_page, name='add_hostel_page'),
    path('add_hostel/', views.add_hostel, name='add_hostel'),
    path('test_page/', views.test_page, name='test_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
