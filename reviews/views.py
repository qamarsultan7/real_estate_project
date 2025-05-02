from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializer import ReviewSerializer
from rest_framework.decorators import api_view


# Create your views here.

@api_view(['POST'])
def addReview(request):
    required_fields = ['review_to', 'review_from', 'giver_image', 'rating', 'review_text']
    for field in required_fields:
        if field not in request.data:
            return Response(
                {
                    "status":False,
                    "message": f"Missing required field: {field}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {  "status":True,
                "message": "Review Added successfully", "user": ReviewSerializer(user).data},
            status=status.HTTP_201_CREATED
        )
    # Validation errors
    return Response(
        {
            "status":False,
            "message": "Validation error", "errors": serializer.errors}, 
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def getReviewsbyId(request, token):
    try:
        # No need to manually parse or check the token format, as Django does that via the <uuid:token> path
    
        reviews = Review.objects.filter(review_to=token)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(
            {
            "status": True,
            "message": "Reviews found", 
            "reviews": serializer.data
            }, 
            status=status.HTTP_200_OK
        )
    except Review.DoesNotExist:
        return Response(
            {
                "status":False,
                "message": "User not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )