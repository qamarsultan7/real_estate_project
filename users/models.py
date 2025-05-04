import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    BUYER = 'buyer'
    SELLER = 'seller'
    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    ]
    name = models.CharField(max_length=255)
    phone = models.BigIntegerField()
    location = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"