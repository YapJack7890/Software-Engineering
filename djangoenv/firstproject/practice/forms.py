from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Student, FoodItem, Request

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('Student_Name', 'Student_Gender', 'Student_Race', 'Student_Grade')

class FoodItemForm(ModelForm):
    class Meta:
        model = FoodItem
        fields = ('Food_Name', 'Food_Price', 'Ingredient_List', 'Food_Description')

class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ('RequestFood_Name', 'RequestFood_Price', 'RequestIngredient_List', 'RequestFood_Description', 'Request_Title')

# class CanteenWorkerForm(ModelForm):
#     class Meta:
#         model = CanteenWorker
#         fields = ('Worker_Username', 'Worker_Password')
