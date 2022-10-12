from django.urls import path

from . import views

urlpatterns = [
   path('login_user', views.login_user, name='login'),
   path('sign_up_user', views.sign_up_user, name='signup'),
   path('logout_user', views.logout_user, name='logout'),



]
