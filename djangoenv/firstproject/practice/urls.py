from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #Authentication
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('', views.loginPage, name='login'),

    #Parent Page
    path('home', views.home, name='home'),
    path('student', views.studentPage, name='student'),
    path('menu/<int:student_id>/', views.menu, name='menu'),
    path('menu/', views.menu, name='menu_without_student'),
    path('foodItem/<int:pk>/<int:student_id>/', views.foodItem, name='fooditem'),
    path('add_to_cart/<str:pk>/', views.add_to_cart, name='add_to_cart'),

    #Admin Page
    path('addfooditem', views.FoodItemPage, name='addfooditem'),
    path('deletefooditem/<str:pk>/', views.deleteFoodItem, name='deletefooditem'),
    path('updatefooditem/<str:pk>/', views.updateFoodItem, name='updatefooditem'),
    path('adminmenu', views.adminmenu, name='adminmenu'),
    path('request_list', views.request_list, name='request_list'),
    path('request_details/<str:pk>/', views.request_details, name='request_details'),

    #Canteen Worker Page
    path('request', views.RequestPage, name='request'),
    path('vieworder', views.view_order, name='vieworder'),


]
