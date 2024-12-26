from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Category,Dish,TableBooking,Cart,CartItem,Order,OrderItem

# Create your views here.

def home(request):
    categorys = Category.objects.all()
    dishes = Dish.objects.all()
    return render(request,'index.html',{'categorys':categorys,'dishes':dishes})

def menu(request):    
    categorys = Category.objects.all()
    dishes = Dish.objects.all()
    return render(request,'menu.html',{'categorys':categorys,'dishes':dishes})
    
@login_required
def book(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        date = request.POST['date']
        time = request.POST['time']
        guests = request.POST['guests']

        max_booking = 10
        exsist_booking = TableBooking.objects.filter(date=date,time=time).count()
        if exsist_booking >= max_booking:
            messages.error(request,"Sorry, no tables are available at this time")
            return redirect('book')
        else:
            booking = TableBooking(
                name=name,
                phone=phone,
                date=date,
                time=time,
                guests=guests,
            )
            if request.user.is_authenticated:
                booking.user = request.user
                booking.save();
                messages.success(request,'Table booked successfully!')
                return redirect('book')
    else:
        return render(request,'book.html')

def about(request):
    return render(request,'about.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exists!')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email already registered!')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                login(request,user)
                messages.success(request,'Signup successfully!')
                return redirect('home')
        else:
            messages.error(request,'Passwords do not match!')
    return render(request,'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'Login successful!')
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('home')


@login_required
def cart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum([item.total_price for item in items])
    return render(request,'cart.html',{'items':items,'total_price':total_price})
@login_required
def add_to_cart(request,dish_id):
    dish = get_object_or_404(Dish,pk=dish_id)
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_item,created = CartItem.objects.get_or_create(cart=cart,dish=dish)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request,f'{dish.name} added to cart successfully!')
    return redirect('menu')

@login_required
def remove_from_cart(request,cart_item_id):
    cart_item = get_object_or_404(CartItem,pk=cart_item_id,cart__user=request.user)
    cart_item.delete()
    messages.success(request,f'{cart_item.dish.name} removed from cart successfully!')
    return redirect('cart')

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first();
    if not cart or not cart.items.exists():
        messages.error(request,"Your cart is empty.")
        return redirect('cart')

    total_price = sum(item.total_price for item in cart.items.all())
    order = Order.objects.create(user=request.user,total_price=total_price)

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            dish=cart_item.dish,
            quantity=cart_item.quantity,
            price=cart_item.dish.price
        )
    
    cart.items.all().delete()
    messages.success(request,"Your order has been placed successfully.")
    return redirect('order_details',order_id=order.id)

@login_required
def order_details(request,order_id):
    order=Order.objects.filter(id=order_id,user=request.user).first()
    if not order:
        messages.error(request,"Order not found")
        return redirect('home')
    
    return render(request,'order_details.html',{'order':order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'orders_list.html',{'orders': orders})