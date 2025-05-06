from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer
from reviews.models import Review
from listed_items.models import ListedItem
from chat.models import ChatRooms, Messages
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def sign_up_user(request):
    email = request.data.get('email')
    
    # Check if required fields are present
    required_fields = ['name', 'phone', 'location', 'email', 'password', 'role']
    for field in required_fields:
        if field not in request.data:
            return Response(
                {
                    "status":False,
                    "message": f"Missing required field: {field}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Check for existing account
    if User.objects.filter(email=email).exists():
        return Response(
            {
                "status":False,
                "message": "Account already exists"},
            status=status.HTTP_409_CONFLICT
        )
    
    # Create new user
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "status": True,
                "message": "User created successfully", 
                "user": UserSerializer(user, context={'request': request}).data
            },
            status=status.HTTP_201_CREATED
        )
    
    # Validation errors
    return Response(
        {
            "status": False,
            "message": "Validation error", 
            "errors": serializer.errors
        }, 
        status=status.HTTP_400_BAD_REQUEST
    )
@api_view(['POST'])
def log_in_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Check if email and password are provided
    if not email or not password:
        return Response(
            {
                "status": False,
                "message": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "status": False,
                "message": "User not found. Please create an account"},
            status=status.HTTP_404_NOT_FOUND
        )

    if not check_password(password, user.password):
        return Response(
            {
                "status": False,
                "message": "Invalid password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return Response({
         "status": True,
        "message": "Login successful",
        "user": UserSerializer(user, context={'request': request}).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_by_id(request, token):
    try:
        # No need to manually parse or check the token format, as Django does that via the <uuid:token> path
        user = User.objects.get(id=token)
        serializer = UserSerializer(user, context={'request': request})
        return Response(
            {
                 "status": True,
                "message": "User found", "user": serializer.data}, 
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {
                 "status": False,
                "message": "User not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        review= Review.objects.filter(review_to=user_id)
        listed_items = ListedItem.objects.filter(agent_id=user_id)
        user.delete()
        review.delete()
        listed_items.delete()
        return Response(
            {
                 "status": True,
                "message": "User deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )
    except User.DoesNotExist:
        return Response(
            {
                 "status": False,
                "message": "User not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    

@api_view(['DELETE'])
def delete_all_users(request):
    try:
        users = User.objects.all()
        reviews = Review.objects.all()
        listed_items = ListedItem.objects.all()
        chat_rooms = ChatRooms.objects.all()
        messages = Messages.objects.all()
        chat_rooms.delete()
        messages.delete()
        users.delete()
        reviews.delete()
        listed_items.delete()
        return Response(
            {
                 "status": True,
                "message": "All users deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {
                 "status": False,
                "message": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )