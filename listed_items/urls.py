from django.urls import path
from .views import ListedItemListView,ListedItemCreateView

urlpatterns = [
    path('properties/', ListedItemListView.as_view(), name='property-list'),
    path('properties/add/', ListedItemCreateView.as_view(), name='property-create'),
]