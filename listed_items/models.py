from django.db import models

# Create your models here.
class ListedItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=255)
    bedroom_count = models.IntegerField()
    bathroom_count = models.IntegerField()
    kitchen_count = models.IntegerField()
    living_room_count = models.IntegerField()
    
    def __str__(self):
        return self.name

class PropertyImage(models.Model):
    property = models.ForeignKey(ListedItem, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    def __str__(self):
        return f"Image for {self.property.name}"