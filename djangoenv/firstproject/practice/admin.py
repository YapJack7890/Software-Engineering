from django.contrib import admin

# Register your models here.
from .models import Student
admin.site.register(Student)

from .models import FoodItem
admin.site.register(FoodItem)

from .models import Request
admin.site.register(Request)

from .models import Cart
admin.site.register(Cart)

from .models import CartItem
admin.site.register(CartItem)

from .models import Order
admin.site.register(Order)
