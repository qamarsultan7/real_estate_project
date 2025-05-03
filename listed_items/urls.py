from django.urls import path
from .views import ListedItemListView,ListedItemCreateView

urlpatterns = [
    path('properties/', ListedItemListView.as_view(), name='property-list'),
     path('properties/create/', ListedItemCreateView.as_view(), name='property-create'),
]