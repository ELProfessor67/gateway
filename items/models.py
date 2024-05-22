from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='src/products/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    quantity = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=100)
    email_address = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    payment = models.IntegerField(default=False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.name



def get_products_by_username(username):
    # Get the user object corresponding to the provided username
    user = User.objects.get(username=username)

    # Retrieve all products associated with the user
    products = Product.objects.filter(owner=user)
    temp = []
    for i in products:
        i.image = str(i.image).replace("src", "")

    return products




