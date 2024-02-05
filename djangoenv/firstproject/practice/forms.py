from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Student, FoodItem, Request

class CreateUserForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

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
