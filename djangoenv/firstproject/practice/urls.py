from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerPage, name='register'),
    path('home', views.home, name='home'),
    path('', views.loginPage, name='login'),
    path('student', views.studentPage, name='student'),
    path('request', views.RequestPage, name='request'),
    path('fooditem/<str:pk>/', views.FoodItemPage, name='fooditem'),
    path('menu', views.menu, name='menu'),
    path('adminmenu', views.adminmenu, name='adminmenu'),
    path('updatefooditem/<str:pk>/', views.updateFoodItem, name='updatefooditem'),
]
