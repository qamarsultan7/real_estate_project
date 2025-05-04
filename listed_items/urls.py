from django.urls import path
from .views import ListedItemListView,ListedItemCreateView,ListedItemUpdateView

urlpatterns = [
    path('properties/', ListedItemListView.as_view(), name='property-list'),
    path('properties/add/', ListedItemCreateView.as_view(), name='property-create'),
    path('properties/<int:pk>/update/', ListedItemUpdateView.as_view(), name='property-update'),
]