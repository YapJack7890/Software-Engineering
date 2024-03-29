from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import CreateUserForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from .models import Student, FoodItem, Request, Order, OrderItem, Cart, CartItem
from .forms import StudentForm, RequestForm, FoodItemForm
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.http import HttpResponse
import qrcode
from io import BytesIO
import base64
from pyzbar.pyzbar import decode
from PIL import Image


#Jakie: Jak12345@
# Create your views here.
def is_canteen_worker(user):
    return user.is_authenticated and user.is_staff

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
            return redirect('user-profile')
        else:
             messages.error(request, 'An error has occurred')

    return render(request, 'register.html', {'form':form})

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('lusername')
        password = request.POST.get('lpassword')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check user type based on model
            if user.is_superuser:
                # User is a superuser
                login(request, user)
                return redirect('admin-menu')  
            elif user.is_staff:
                # User is a valid CanteenWorker
                login(request, user)
                return redirect("canteen-orderlist")
            else:
                # User is a regular user
                login(request, user)
                return redirect('user-profile') 
        else:
            messages.error(request, "Invalid username or password")

    context = {'page': page}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('register')

#Below functions are for parent page
@login_required(login_url='register')
def home(request):
    studentform = StudentForm()
    
    if request.method == 'POST':
        studentform = StudentForm(request.POST)
        if studentform.is_valid():
            student_form = studentform.save(commit=False)
            student_form.Parent = request.user
            student_form.save()
            return redirect('user-profile')
        else:
             messages.error(request, 'An error has occurred')

    current_user = request.user

    current_user = request.user
    students = Student.objects.filter(Parent=current_user)

    order_items_by_order = {}

    for student in students:
        order_items = OrderItem.objects.filter(order__cart__student=student).select_related('order__cart__student', 'order_item')
        
        for order_item in order_items:
            order = order_item.order
            #Check if Order is already a key in the dictionary
            if order not in order_items_by_order:
                #If not, add a new key with an empty list
                order_items_by_order[order] = []
            #Append the current OrderItem to the list associated with the Order
            order_items_by_order[order].append(order_item)

    #students = Student.objects.filter(Parent=current_user)
    
    # Create a list to store each student's cart
    carts = []
    for student in students:
        # Access the related cart for each student
        cart = student.cart
        carts.append(cart)
    return render(request, 'user-profile.html', {'order_items_by_order': order_items_by_order, 'students': students, 'carts': carts, 'form':studentform})

@login_required(login_url='register')
def editStudent(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
        else:
             messages.error(request, 'An error has occurred')
        
    context = {'form': form, 'student': student}
    return render(request, 'student.html', context)

@login_required(login_url='register')
def menu(request, student_id):
    if student_id is not None:
        # Get the current student based on the provided student_id
        current_student = get_object_or_404(Student, id=student_id)
        print(f"Current Student: {current_student}")  # Print the current student information
    else:
        # Handle the case when student_id is not provided
        current_student = None

    #Filters FoodItem objects where Food_Availability is True
    available_food_items = FoodItem.objects.filter(Food_Availability=True)
    return render(request, 'user-menu.html', {'fooditems': available_food_items, 'current_student': current_student})

@login_required(login_url='register')
def foodItem(request, pk, student_id):
    # Get the current student based on the provided student_id
    current_student = get_object_or_404(Student, id=student_id)

    # Fetch the FoodItem object based on the provided pk
    fooditem = FoodItem.objects.get(id=pk)

    context = {'fooditem': fooditem, 'current_student': current_student}
    return render(request, 'fooditem.html', context)

@login_required(login_url='register')
def add_to_cart(request, pk, student_id):
    # Get the product based on the product_id
    fooditem = get_object_or_404(FoodItem, id=pk)
    print(f"Student ID: {student_id}")  

    # Get the Student instance based on the student_id
    current_student = get_object_or_404(Student, id=student_id)
    print(f"Student: {current_student}")
    # Check if the user has a student
    if current_student is None:
        #redirect to student page 
        messages.warning(request, 'A student profile is needed to add food item to cart')
        return redirect('user-profile') 

    # Check if the student has a cart
    if not hasattr(current_student, 'cart'):
        Cart.objects.create(student=current_student)

    # Now, the student should have a cart. Get the cart.
    cart = current_student.cart

    # Get the quantity from the form data
    quantity = int(request.POST.get('quantity', 1))

    # Check if the product is already in the cart, update quantity if yes, create a new item if not
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, cart_item=fooditem)

    # Update quantity based on the selected value
    if not item_created:
        # If the item already exists in the cart, increase the quantity by the specified quantity
        cart_item.cartitem_quantity += quantity
    else:
        # If the item is newly added to the cart, set the quantity to the specified quantity
        cart_item.cartitem_quantity = max(1, quantity)
    cart_item.save()
        # Redirect to 'menu' with the student_id parameter
    return redirect('user-menu', student_id = student_id)

@login_required(login_url='register')
def display_cart(request, student_id):
        # Retrieve the Cart instance using the provided student_id
        cart = get_object_or_404(Cart, student_id=student_id)

        # Retrieve all CartItem instances associated with the Cart
        cart_items = CartItem.objects.filter(cart=cart)
        
        # Prepare data for rendering (this can be improved with templates)
        cart_data = []
        total_price = 0  # Initialize total price
        cart_item = None  # Initialize cart_item
        for cart_item in cart_items:
            item_data = {
                'id': cart_item.id,
                'name': cart_item.cart_item.Food_Name,
                'price': cart_item.cart_item.Food_Price,
                'quantity': cart_item.cartitem_quantity,
                'total_price': cart_item.total_price(),
            }
            cart_data.append(item_data)

            # Accumulate the total price
            total_price += cart_item.total_price()

        return render(request, 'cart.html', {'student_id': student_id, 'cart_data': cart_data, 'cart': cart, 'cart_item': cart_item, 'cart_total_price': total_price})
    
@login_required(login_url='register')
def increase_cart_item_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    # Increase the quantity by 1
    cart_item.cartitem_quantity += 1
    cart_item.save()

    return redirect('cart', student_id=cart_item.cart.student.id)

@login_required(login_url='register')
def decrease_cart_item_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)

    if cart_item.cartitem_quantity > 1:
        # Decrease the quantity by 1, but ensure it stays at least 1
        cart_item.cartitem_quantity = max(1, cart_item.cartitem_quantity - 1)
        cart_item.save()
    else: 
        # If the quantity is 1, remove the item from the cart
        cart_item.delete()

    return redirect('cart', student_id=cart_item.cart.student.id)

@login_required(login_url='register')
def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()

    return redirect('cart', student_id=cart_item.cart.student.id)

@login_required(login_url='register')
def order_history(request):
    current_user = request.user
    students = Student.objects.filter(Parent=current_user)

    order_items_by_order = {}

    for student in students:
        order_items = OrderItem.objects.filter(order__cart__student=student).select_related('order__cart__student', 'order_item')
        
        for order_item in order_items:
            order = order_item.order
            #Check if Order is already a key in the dictionary
            if order not in order_items_by_order:
                #If not, add a new key with an empty list
                order_items_by_order[order] = []
            #Append the current OrderItem to the list associated with the Order
            order_items_by_order[order].append(order_item)
    return render(request, 'user-profile.html', {'order_items_by_order': order_items_by_order})

@login_required(login_url='register')
def checkout(request, cart_id):
        # Retrieve the Cart instance using the cart_id
        cart = get_object_or_404(Cart, id=cart_id)

        # Retrieve all CartItem instances associated with the Cart
        cart_items = CartItem.objects.filter(cart=cart)
    
        if not cart_items.exists():
            return redirect('cart', student_id=cart.student.id)
        # Prepare data for rendering
        cart_data = []
        total_price = 0  # Initialize total price
        cart_item = None  # Initialize cart_item
        for cart_item in cart_items:
            item_data = {
                'id': cart_item.cart_item.id,
                'name': cart_item.cart_item.Food_Name,
                'quantity': cart_item.cartitem_quantity,
                'total_price': cart_item.total_price(),
            }
            cart_data.append(item_data)

            # Accumulate the total price
            total_price += cart_item.total_price()

        # Return a simple HTML response (this can be improved with templates)
        return render(request, 'checkout.html', {'cart_data': cart_data, 'cart': cart, 'cart_item': cart_item, 'total_price': total_price})

@login_required(login_url='register')
def place_order(request, cart_id):
    # Get the product based on the product_id
    cart = get_object_or_404(Cart, id=cart_id)
    cart_items = CartItem.objects.filter(cart=cart)

    order = Order.objects.create(cart=cart, order_total_price=0)

    total_price = 0

    for cart_item in cart_items:
        order_item = OrderItem.objects.create(
            order=order,
            order_item=cart_item.cart_item,
            orderitem_quantity=cart_item.cartitem_quantity,
            order_item_total_price=cart_item.total_price(),
        )

        total_price += order_item.order_item_total_price

    # Update the total_price in the Order model
    order.order_total_price = total_price
    order.save()

    # delete cart items after saved as order
    cart_items.delete()

    return JsonResponse({'success': True, 'message': 'Order placed successfully'})

#Below functions are for CanteenWorker page
@user_passes_test(is_canteen_worker, login_url='login')
def view_orders_canteen(request):

    orders = Order.objects.all()  # Fetch all Order objects

    orders_data = []

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)

        order_data = {
            'order_id': order.id,
            'total_price': order.order_total_price,
            'status': order.Order_Status,
            'order_items': [],
        }
        print("Order status: ")
        print(order.Order_Status)
        for order_item in order_items:
            item_data = {
                'food_item_name': order_item.order_item.Food_Name,
                'quantity': order_item.orderitem_quantity,
                'total_price': order_item.order_item_total_price,
            }
            order_data['order_items'].append(item_data)

        orders_data.append(order_data)

    # Pass data to the template
    context = {'orders_data': orders_data}
    return render(request, 'canteen-orderlist.html', context)

@user_passes_test(is_canteen_worker, login_url='login')
def RequestPage(request):
    form = RequestForm()
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            #user = form.save(commit=False)
            form.save()
            # Redirect to a new page
            return redirect('canteen-request')
        else:
             messages.error(request, 'An error has occurred')


    return render(request, 'canteen-request.html', {'form':form})
    
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
            return redirect('admin-menu')
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
            return redirect('admin-menu')
        else:
             messages.error(request, 'An error has occurred')
        
    context = {'form': form}
    return render(request, 'addfooditem.html', context)

@user_passes_test(is_superuser, login_url='login')
def deleteFoodItem(request, pk):
    fooditem = FoodItem.objects.get(id=pk)
    if request.method == 'POST':
        fooditem.delete()
        return redirect('admin-menu')
    context = {'obj': fooditem}
    return render(request, 'delete.html', context)

@user_passes_test(is_superuser, login_url='login')
def adminmenu(request):

    fooditems = FoodItem.objects.all()  # Fetch all FoodItem objects
    return render(request, 'admin-menu.html', {'fooditems': fooditems})

def adminfoodItem(request, pk):
    # Fetch the FoodItem object based on the provided pk
    fooditem = FoodItem.objects.get(id=pk)

    context = {'fooditem': fooditem, }
    return render(request, 'adminfooditem.html', context)

def toggle_availability(request, fooditem_id):
    # Retrieve the FoodItem object
    fooditem = FoodItem.objects.get(pk=fooditem_id)
    
    # Toggle the availability
    fooditem.Food_Availability = not fooditem.Food_Availability
    
    # Save the changes
    fooditem.save()
    
    # Redirect back to the menu page
    return redirect('admin-menu')

@user_passes_test(is_superuser, login_url='login')
def view_orders(request):

    orders = Order.objects.all()  # Fetch all Order objects

    orders_data = []

    for order in orders:
        order_items = OrderItem.objects.filter(order=order)

        order_data = {
            'order_id': order.id,
            'total_price': order.order_total_price,
            'order_items': [],
        }

        for order_item in order_items:
            item_data = {
                'food_item_name': order_item.order_item.Food_Name,
                'quantity': order_item.orderitem_quantity,
                'total_price': order_item.order_item_total_price,
            }
            order_data['order_items'].append(item_data)

        orders_data.append(order_data)

    # Pass data to the template
    context = {'orders_data': orders_data}
    return render(request, 'admin-orderlist.html', context)


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
                                            Food_Description=request_obj.RequestFood_Description)
                    request_obj.delete()  # Delete the request after processing

                elif action == 'deny':
                    print("Denying request...")
                    request_obj.delete()  # Simply delete the request
            except Request.DoesNotExist:
                pass
    requests = Request.objects.all()
    return render(request, 'admin-request.html', {'requests': requests})

@user_passes_test(is_superuser, login_url='login')
def request_details(request, pk):
    request_details = Request.objects.get(id=pk)
    context = {'request_details': request_details}
    return render(request, 'request_details.html', context)

@user_passes_test(is_superuser, login_url='login')
def worker_register(request):
    workerform = CreateUserForm()
    if request.method == 'POST':
        workerform = CreateUserForm(request.POST)
        if workerform.is_valid():
            worker_form = workerform.save(commit=False)
            worker_form.is_staff = True
            worker_form.save()
            return redirect('admin-menu')
        else:
            messages.error(request, 'An error has occurred')

    return render(request, 'worker_register.html', {'form':workerform})

#Yap Choo Kath Moon
#1211102270
def forget_password(request):
    return render(request, 'forget-password.html')

def generate_qrcode(request, order_id):
    # Get the order based on the provided order_id
    order = Order.objects.get(id=order_id)
    
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(order.id)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the imamge into memory
    response = BytesIO()
    img.save(response, 'PNG')
    response.seek(0)
    
    # Convert the image to a data URL
    img_data = base64.b64encode(response.getvalue()).decode('ascii')
    img_data_url = 'data:image/png;base64,' + img_data
    
    # Pass the data URL to the template context
    context = {'img_data_url': img_data_url}
    return render(request, 'viewQR.html', context)

def get_order_details(request, order_id):
    # Get the order based on the provided order_id
    print(f'order_id: {order_id}')
    order = Order.objects.get(id=order_id)
    # Get the order items and their quantities
    print(f'order: {order}')
    order_items = OrderItem.objects.filter(order=order)
    print(f'order_items: {order_items}')
    order_data = {
        'order_id': order.id,
        'total_price': order.order_total_price,
        'order_items': [],
    }

    for order_item in order_items:
        item_data = {
            'food_item_name': order_item.order_item.Food_Name,
            'quantity': order_item.orderitem_quantity,
            'total_price': order_item.order_item_total_price,
        }
        order_data['order_items'].append(item_data)

    # Pass the order data to the template context
    context = {'order_data': order_data}
    print(f'context: {context}') 
    return render(request, 'canteen-qrcode.html', context)

def scan_qr_code(qr_code_image):
    # Convert the uploaded file to an image
    image = Image.open(qr_code_image)

    # Decode the QR code
    decoded_objects = decode(image)

    # Extract the order_id from the decoded objects
    # This assumes that the order_id is the only data in the QR code
    order_id = int(decoded_objects[0].data.decode("utf-8"))
    # Update the order status to "Received"
    order = Order.objects.get(order_id=order_id)
    order.Order_Status = "Received"
    order.save()
    return order_id

def upload_qr(request):
    if request.method == 'POST':
        qr_code_image = request.FILES['qr_code']
        # scan the QR code and extract the order_id
        order_id = scan_qr_code(qr_code_image)
        # redirect to the 'get_order_details' view with the order_id as an argument
        return redirect('get_order_details', order_id=order_id)
    return render(request, 'upload_qr.html')
