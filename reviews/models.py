import uuid
from django.db import models

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    review_to = models.UUIDField(default=uuid.uuid4)   # The user who receives the review
    review_from = models.UUIDField(default=uuid.uuid4) # The user who gives the review
    giver_image = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    review_text = models.TextField()
    def __str__(self):
        return f"Review {self.id} from {self.review_from} to {self.review_to}"
