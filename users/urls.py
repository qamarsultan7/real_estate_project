from django.urls import path
from .views import sign_up_user, log_in_user, get_user_by_id, delete_user,delete_all_users

urlpatterns = [
    path('signup/', sign_up_user, name='signup'),
    path('login/', log_in_user, name='login'),
    path('remove/<str:user_id>/', delete_user, name='user_profile'),  # Handle string user_id in path
    path('remove-all/', delete_all_users, name='remoe-all'),  # Handle string user_id in path
    path('profile/<uuid:token>/', get_user_by_id, name='user_profile_path'),  # Handle UUID in path
]