from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class Parent(models.Model):
#    Parent = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
#    Parent_Phone_Num = models.IntegerField('Parent Phone Number')
#    Parent_Username = models.CharField('Parent Username', max_length=50)
#    Parent_Password = models.CharField('Parent Password', max_length=50)
#    Parent_Email = models.EmailField('Parent Email', max_length=50)
class Student(models.Model):
    Parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Student_Name = models.CharField('Student Name', max_length=50)
    Student_Gender = models.CharField('Student Gender', max_length=10)
    Student_Race = models.CharField('Student Race', max_length=10)
    Student_Grade = models.IntegerField('Student Grade')
    #Student_Created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Student_Name

class FoodItem(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Food_Name = models.CharField('Food Name', max_length=50)
    Food_Price = models.DecimalField('Food Price',max_digits=4, decimal_places=2)
    #Food_Image = models.ImageField('Food Image', upload_to='food_pictures/')
    Ingredient_List = models.TextField('Ingredient List', max_length=100)
    Food_Description = models.TextField('Food Description', max_length=200)
    Food_Category = models.CharField('Food Category', max_length=10)

    def _str_(self):
        return self.Food_Name


class Request(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    RequestFood_Name = models.CharField('Request Food Name', max_length=50)
    RequestFood_Price = models.DecimalField('Request Food Price',max_digits=4, decimal_places=2)
    #RequestFood_Image = models.ImageField('Request Food Image', upload_to='food_pictures/')
    RequestIngredient_List = models.TextField('Request Ingredient List', max_length=100)
    RequestFood_Description = models.TextField('Request Food Description', max_length=200)
    RequestFood_Category = models.CharField('Request Food Category', max_length=10)
    Request_Title = models.CharField('Request Title', max_length=50)

    def _str_(self):
        return self.RequestFood_Name


class Order(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    food = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    Order_Status = models.CharField('Order Status', max_length=10)

    #def _str_(self):
    #    return self.id

class CanteenWorker(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Worker_Username = models.CharField('Canteen Worker Username', max_length=50)
    Worker_Password = models.CharField('Canteen Worker Password', max_length=50)

    def _str_(self):
        return self.Worker_Username

