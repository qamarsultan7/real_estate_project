from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializer import UserSerializer
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
                "message": "User created successfully", "user": UserSerializer(user).data},
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
        "user": UserSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_by_id(request, token):
    try:
        # No need to manually parse or check the token format, as Django does that via the <uuid:token> path
        user = User.objects.get(id=token)
        serializer = UserSerializer(user)
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