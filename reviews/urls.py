from django.urls import path
from .views import getReviewsbyId,addReview

urlpatterns=[
    path('add/',addReview,name='addReview'),
    path('<uuid:token>/',getReviewsbyId,name='getReviewsbyId')
]