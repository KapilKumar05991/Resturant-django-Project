from django.contrib import admin
from .models import Category,Dish,TableBooking,Cart,CartItem,Order,OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(TableBooking)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
