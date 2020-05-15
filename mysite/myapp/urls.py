from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('show_user_content/<slug:username>/<slug:rand_code>/', views.show_user_content, name='show_user_content'),
    path('register_myuser_page/', views.register_myuser_page, name='register_myuser_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
]