from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import CreateUserForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from .models import Student, FoodItem, Request, Order, CanteenWorker, Cart, CartItem
from .forms import StudentForm, RequestForm, FoodItemForm
from django.views import View
from django.contrib.auth.decorators import user_passes_test

#Jakie: Jak12345@
# Create your views here.
def is_canteen_worker(user):
    return user.is_authenticated and hasattr(user, 'CanteenWorker')

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

#below functions are authentications
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

'''
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
'''
def loginPage(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check user type based on model
            if hasattr(user, 'CanteenWorker'):
                # User is a CanteenWorker
                login(request, user)
                return redirect('vieworder')  # Adjust to your canteen page URL
            elif user.is_superuser:
                # User is a superuser
                login(request, user)
                return redirect('adminmenu')  # Adjust to your admin page URL
            else:
                # User is a regular user
                login(request, user)
                return redirect('home')  # Adjust to your user page URL
        else:
            messages.error(request, "Invalid username or password")

    context = {'page': page}
    return render(request, 'register_login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('register')

#Below functions are for parent page
@login_required(login_url='register')
def home(request):
    current_user = request.user
    #user_id = current_user.id
    #context = {'user_id': user_id}
    students = Student.objects.filter(Parent=current_user)  # Fetch all student objects
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

@login_required(login_url='register')
def menu(request, student_id):
    if student_id is not None:
        # Get the current student based on the provided student_id
        current_student = get_object_or_404(Student, id=student_id)
    else:
        # Handle the case when student_id is not provided
        current_student = None

    # Fetch all FoodItem objects
    fooditems = FoodItem.objects.all()  # Fetch all FoodItem objects
    return render(request, 'menu.html', {'fooditems': fooditems, 'current_student': current_student})

@login_required(login_url='register')
def foodItem(request, pk, student_id):
    # Get the current student based on the provided student_id
    current_student = get_object_or_404(Student, id=student_id)

    # Fetch the FoodItem object based on the provided pk
    foodItem = FoodItem.objects.get(id=pk)

    context = {'fooditem': foodItem, 'current_student': current_student}
    return render(request, 'fooditem.html', context)


def add_to_cart(request, pk):
    # Get the product based on the product_id
    foodItem = get_object_or_404(FoodItem, id=pk)

    # Check if the user has a student, create one if not
    if not hasattr(request.user, 'student'):
        #redirect to student page 
        messages.warning(request, 'A student profile is needed to add food item to cart')
        return redirect('student') 
    # Now, the user should have a student. Get the student.
    student = request.user.student

    if not hasattr(request.user, 'cart'):
        Cart.objects.create(student=student)

    # Now, the student should have a cart. Get the cart.
    cart = student.cart

    # Get the quantity from the form data
    quantity = int(request.POST.get('quantity', 1))

    # Check if the 'add_to_cart' button was pressed
    if 'add_to_cart' in request.POST:
    # Check if the product is already in the cart, update quantity if yes, create a new item if not
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food_item=foodItem)

        if not item_created:
            # Update quantity based on the selected value
            cart_item.quantity += quantity
            # Ensure the quantity is not less than 1
            cart_item.quantity = max(1, cart_item.cartitem_quantity)
            cart_item.save()
        return redirect('menu')

    return render(request, 'fooditem.html', {'fooditem': foodItem})

def place_order(request):
    # Let's assume a user is already authenticated, you might want to handle authentication in a real-world scenario
    user = User.objects.get(django_user=request.user)

    # Assume we have some food items available in the database
    food_items = FoodItem.objects.all()

    if request.method == 'POST':
        selected_food_items = request.POST.getlist('food_items')
        quantity = int(request.POST.get('quantity', 1))
        order_status = request.POST.get('order_status', 'Pending')

        # Create a new order
        order = Order.objects.create(
            user=user,
            quantity=quantity,
            order_status=order_status,
        )
        # Add selected food items to the order
        order.food_items.set(selected_food_items)

        return render(request, 'order_placed.html', {'order': order})

    return render(request, 'place_order.html', {'food_items': food_items})

#Below functions are for CanteenWorker page
@user_passes_test(is_canteen_worker, login_url='login')
def RequestPage(request):
    form = RequestForm()
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            #user = form.save(commit=False)
            form.save()
            #login(request, form)
            return redirect('home')
        else:
             messages.error(request, 'An error has occurred')


    return render(request, 'request.html', {'form':form})

@login_required(login_url='register')
def view_order(request):

    order = Order.objects.all()  # Fetch all Order objects
    return render(request, 'vieworder.html', {'order': order})
    
#Below functions are for admin page
@user_passes_test(is_superuser, login_url='login')
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

@user_passes_test(is_superuser, login_url='login')
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

@user_passes_test(is_superuser, login_url='login')
def deleteFoodItem(request, pk):
    fooditem = FoodItem.objects.get(id=pk)
    if request.method == 'POST':
        fooditem.delete()
        return redirect('adminmenu')
    context = {'obj': fooditem}
    return render(request, 'delete.html', context)



@user_passes_test(is_superuser, login_url='login')
def adminmenu(request):

    fooditems = FoodItem.objects.all()  # Fetch all FoodItem objects
    return render(request, 'adminmenu.html', {'fooditems': fooditems})


@user_passes_test(is_superuser, login_url='login')
def request_list(request):
    print(f"Method: {request.method}")
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        print(f"Received POST request. Request ID: {request_id}, Action: {action}")

        if request_id and action:
            try:
                request_obj = Request.objects.get(pk=request_id)
                print(f"Request_obj: {request_obj}")

                if action == 'accept':
                    print("Accepting request...")
                    # Assuming FoodItem has fields like 'name' and 'description'
                    FoodItem.objects.create(Food_Name=request_obj.RequestFood_Name, 
                                            Food_Price=request_obj.RequestFood_Price,
                                            Ingredient_List=request_obj.RequestIngredient_List, 
                                            Food_Description=request_obj.RequestFood_Category,
                                            Food_Category=request_obj.RequestFood_Category)
                    request_obj.delete()  # Delete the request after processing

                elif action == 'deny':
                    print("Denying request...")
                    request_obj.delete()  # Simply delete the request
            except Request.DoesNotExist:
                pass
    requests = Request.objects.all()
    return render(request, 'request_list.html', {'requests': requests})

@user_passes_test(is_superuser, login_url='login')
def request_details(request, pk):
    request_details = Request.objects.get(id=pk)
    context = {'request_details': request_details}
    return render(request, 'request_details.html', context)

@user_passes_test(is_superuser, login_url='login')
def worker_register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
        else:
             messages.error(request, 'An error has occurred')

    return render(request, 'worker_register.html', {'form':form})
