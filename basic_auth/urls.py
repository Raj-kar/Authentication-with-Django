from django.urls import path

from . import views

# Template tagging
app_name = 'basic_auth'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('special/', views.special, name='secret'),
]
