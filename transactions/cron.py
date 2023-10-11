from django.contrib.auth.models import User
from .models import MerchantsKey

# limiter
def limiter():
    users = User.objects.all()
    for user in users:
        merchant_key = MerchantsKey.objects.filter(username=user.username).first()
        if merchant_key is not None:
            shuffled_key = merchant_key.shuffling_key()
            merchant_key.key = shuffled_key
            merchant_key.save()
