from django.db import models

# Create your models here.

class ListedItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bedroom_count = models.IntegerField()
    bathroom_count = models.IntegerField()
    garage_count = models.IntegerField()

    def __str__(self):
        return self.name