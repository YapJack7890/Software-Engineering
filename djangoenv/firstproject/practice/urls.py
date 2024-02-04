from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #Authentication
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('', views.loginPage, name='login'),
    path('reset_password', views.forget_password, name="reset_password"),

    #Parent Page
    path('home', views.home, name='home'),
    path('student', views.studentPage, name='student'),
    path('menu/<int:student_id>/', views.menu, name='menu'),
    path('menu/', views.menu, name='menu_without_student'),
    path('foodItem/<int:pk>/<int:student_id>/', views.foodItem, name='fooditem'),
    path('add_to_cart/<str:pk>/<int:student_id>/', views.add_to_cart, name='add_to_cart'),
    path('display_cart/<int:student_id>/', views.display_cart, name='display_cart'),
    path('increase_cart_item_quantity/<int:cart_item_id>/', views.increase_cart_item_quantity, name='increase_cart_item_quantity'),
    path('decrease_cart_item_quantity/<int:cart_item_id>/', views.decrease_cart_item_quantity, name='decrease_cart_item_quantity'),
    path('remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/<int:cart_id>/', views.checkout, name='checkout'),
    path('place_order/<int:cart_id>/', views.place_order, name='place_order'),

    #Admin Page
    path('addfooditem', views.FoodItemPage, name='addfooditem'),
    path('deletefooditem/<str:pk>/', views.deleteFoodItem, name='deletefooditem'),
    path('updatefooditem/<str:pk>/', views.updateFoodItem, name='updatefooditem'),
    path('adminmenu', views.adminmenu, name='adminmenu'),
    path('adminfoodItem/<int:pk>/', views.adminfoodItem, name='adminfooditem'),
    path('request_list', views.request_list, name='request_list'),
    path('request_details/<str:pk>/', views.request_details, name='request_details'),


    #Canteen Worker Page
    path('request', views.RequestPage, name='request'),
    path('vieworders', views.view_orders, name='vieworders'),


]
