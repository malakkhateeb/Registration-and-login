from django.urls import path     
from . import views

urlpatterns = [
    path('', views.logIn),
    path('register', views.addRegistrations),
    path('login', views.addLogin),
    path('success', views.showLogin),
    path('logout',views.logOut)

]