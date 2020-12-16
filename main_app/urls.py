from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home_page/', views.home_page, name='home_page'),
    path('student_home_page/', views.student_home_page, name='student_home_page'),
    path('hostel_owner_home_page/', views.hostel_owner_home_page, name='hostel_owner_home_page'),
    path('add_hostel_page/', views.add_hostel_page, name='add_hostel_page'),
    path('add_hostel/', views.add_hostel, name='add_hostel'),
    path('test_page/', views.test_page, name='test_page'),
]
