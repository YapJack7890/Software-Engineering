from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Student, FoodItem, Request, Order, CanteenWorker
from .forms import StudentForm, RequestForm, FoodItemForm

#Jakie: Jak12345@
# Create your views here.
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
        username = request.POST.get('username')
        password = request.POST['password']
        
        #check if it exist
        #try:
        #    user = User.objects.get(email=email)
        #except: 
        #    messages.error(request, "Email does not exist")
        #make sure info is right
        user = authenticate(request, username=username, password=password)
        #login
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
           messages.error(request, ("Email does not exit or password is wrong"))

    context = {'page': page}
    return render(request, 'register_login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('register')

@login_required(login_url='register')
def home(request):

    students = Student.objects.all()  # Fetch all student objects
    return render(request, 'home.html', {'students': students})


@login_required(login_url='register')
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

#menu
@login_required(login_url='register')
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

def foodItem(request, pk):
    foodItem = FoodItem.objects.get(id=pk)
    context = {'foodItem': foodItem}
    return render(request, 'fooditem.html', context)
    
@login_required(login_url='register')
def FoodItemPage(request):
    form = FoodItemForm()
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            #user = form.save(commit=False)
            form.save()
            #login(request, form)
            return redirect('adminmenu')
        else:
             messages.error(request, 'An error has occurred')


    return render(request, 'addfooditem.html', {'form':form})

@login_required(login_url='register')
def updateFoodItem(request, pk):
    fooditem = FoodItem.objects.get(id=pk)
    form = FoodItemForm(instance=fooditem)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=fooditem)
        if form.is_valid():
            form.save()
            return redirect('adminmenu')
        else:
             messages.error(request, 'An error has occurred')
        
    context = {'form': form}
    return render(request, 'addfooditem.html', context)

@login_required(login_url='register')
def deleteFoodItem(request, pk):
    fooditem = FoodItem.objects.get(id=pk)
    if request.method == 'POST':
        fooditem.delete()
        return redirect('adminmenu')
    context = {'obj': fooditem}
    return render(request, 'delete.html', context)

@login_required(login_url='register')
def menu(request):

    fooditems = FoodItem.objects.all()  # Fetch all student objects
    return render(request, 'menu.html', {'fooditems': fooditems})

@login_required(login_url='register')
def adminmenu(request):

    fooditems = FoodItem.objects.all()  # Fetch all student objects
    return render(request, 'adminmenu.html', {'fooditems': fooditems})

#def cart(request):
#    return{'cart': Cart(request)}

#cart
#@login_required(login_url='register')
#def cart_summary(request): 
    #get the cart
#    cart = Cart(request)

#    if request.POST.get('action') == 'post':
        #get food item
#        FoodItem_id = int(request.POST.get('FoodItem.id'))
#        content = {{}}
#    return render(request, 'cart_summary.html', content)

#@login_required(login_url='register')
#def cart_add(request): 
#    pass

#@login_required(login_url='register')
#def cart_delete(request): 
#    pass

##@login_required(login_url='register')
#def cart_update(request): 
#    pass
