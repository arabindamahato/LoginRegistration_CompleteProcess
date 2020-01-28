from django.urls import path
from myapp import views

app_name = 'myapp'


urlpatterns = [
    path('register/', views.registration, name = 'register'),
    path('login/', views.user_login, name = 'login'),
] 