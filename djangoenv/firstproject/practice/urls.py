from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('home', views.home, name='home'),
    path('', views.loginPage, name='login'),
    path('student', views.studentPage, name='student'),
    path('request', views.RequestPage, name='request'),
    path('addfooditem', views.FoodItemPage, name='fooditem'),
    path('deletefooditem/<str:pk>/', views.deleteFoodItem, name='deletefooditem'),
    path('fooditem/<str:pk>/', views.foodItem, name='fooditem'),
    path('menu', views.menu, name='menu'),
    path('adminmenu', views.adminmenu, name='adminmenu'),
    path('updatefooditem/<str:pk>/', views.updateFoodItem, name='updatefooditem'),
    #path('cart_summary', views.cart_summary, name='cart_summary'),
    #path('cart_add', views.cart_add, name="cart_add"),
    #path('cart_delete', views.cart_delete, name="cart_delete"),
    #path('cart_update', views.cart_update, name="cart_update"),
]
