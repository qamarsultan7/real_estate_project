from django.urls import path
from .views import sign_up_user, log_in_user, get_user_by_id

urlpatterns = [
    path('signup/', sign_up_user, name='signup'),
    path('login/', log_in_user, name='login'),
    path('profile/<uuid:token>/', get_user_by_id, name='user_profile_path'),  # Handle UUID in path
]