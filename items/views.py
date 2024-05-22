from django.shortcuts import render, redirect, HttpResponse
from .models import Product, get_products_by_username,Order
from django.contrib.auth.decorators import login_required
from transactions.forms import TransactionForm

login_required(login_url="/")
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('file')
        print(image)

        # Save the product to the database
        product = Product(
            name=name,
            description=description,
            category=category,
            price=price,
            stock=stock,
            image=image,
            owner=request.user
        )
        product.save()

        return redirect('/items/all')
    return render(request,'items/add.html')


login_required(login_url="/")
def all(request):
    # Assuming the current user is authenticated
    username = request.user.username
    products = get_products_by_username(username)
    
    # Now you can pass the products to your template or do further processing
    # For example:
    return render(request, 'items/all.html', {'products': products})



def single_product(request,id):
    product = Product.objects.get(pk=id)
    product.image = str(product.image).replace("src", "")
    isStock = True
    if(product.stock == 0 ):
        isStock = False
    return render(request,'items/single_product.html',{"product": product,"stock":isStock})

def order_product(request,id):
    if request.method == "POST":
        order = Order.objects.get(pk=id)
        order.payment = True
        order.save()
        return HttpResponse("Order Placed Succesfully")
    return render(request,'items/order_page.html')


def chechout(request,id):
    if request.method == 'POST':
        # Retrieve customer data from request.POST
        name = request.POST.get('name')
        email_address = request.POST.get('email_address')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        
        # Retrieve order data from request.POST
        quantity = request.POST.get('quantity')
        product = Product.objects.get(pk=id)
        
        # Create and save the Order object
        order = Order.objects.create(
            quantity=quantity,
            name=name,
            email_address=email_address,
            phone=phone,
            address=address,
            city=city,
            postal_code=postal_code,
            product=product,
            payment=False,
            owner=product.owner
        )
        
        return redirect('/items/order/'+str(order.id))
    return render(request,'items/checkout_page.html')



def all_orders(request):
    orders = Order.objects.filter(owner=request.user,payment=True)
    return render(request,'items/orders.html',{"orders":orders})