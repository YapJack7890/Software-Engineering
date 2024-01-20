from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Student, FoodItem, Request, Order, CanteenWorker
from .forms import StudentForm, RequestForm, FoodItemForm

# Create your views here.
@login_required(login_url='register')
def home(request):

    students = Student.objects.all()  # Fetch all student objects
    return render(request, 'home.html', {'students': students})


def registerPage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'An error has occurred')

    return render(request, 'register_login.html', {'form':form})

#
def loginPage(request):
    page = 'login'
    #get user
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        #check if it exist
        #try:
        #    user = User.objects.get(email=email)
        #except: 
        #    messages.error(request, "Email does not exist")
        #make sure info is right
        user = authenticate(request, email=email, password=password)
        #login
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, ("Email does not exit or password is wrong"))

    context = {'page': page}
    return render(request, 'register_login.html', context)

def studentPage(request):
    studentform = StudentForm()
    
    if request.method == 'POST':
        studentform = StudentForm(request.POST)
        if studentform.is_valid():
            #user = form.save(commit=False)
            studentform.save()
            #login(request, studentform)
            return redirect('home')
        else:
             messages.error(request, 'An error has occurred')


    return render(request, 'student.html', {'form':studentform})

def RequestPage(request):
    form = RequestForm()
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            #user = form.save(commit=False)
            form.save()
            login(request, form)
            return redirect('home')
        else:
             messages.error(request, 'An error has occurred')


    return render(request, 'request.html', {'form':form})

def FoodItemPage(request):
    form = FoodItemForm()
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            #user = form.save(commit=False)
            form.save()
            #login(request, form)
            return redirect('home')
        else:
             messages.error(request, 'An error has occurred')


    return render(request, 'fooditem.html', {'form':form})

def updateFoodItem(request, pk):
    fooditem = FoodItem.objects.get(id=pk)
    form = FoodItemForm(instance=fooditem)
    if request.method=='POST':
        form == FoodItemForm(request.POST, instance=fooditem)
        if form.is_valid():
            form.save()
            return redirect('menu')
    context = {'form': form}
    return render(request, 'menu.html', context)

def menu(request):

    fooditems = FoodItem.objects.all()  # Fetch all student objects
    return render(request, 'menu.html', {'fooditems': fooditems})

def adminmenu(request):

    fooditems = FoodItem.objects.all()  # Fetch all student objects
    return render(request, 'adminmenu.html', {'fooditems': fooditems})
