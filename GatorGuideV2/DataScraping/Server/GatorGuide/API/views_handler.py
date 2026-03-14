from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import UserSerializer
from .models import User
# Create your views here.

# Write your create_user function here
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# Write your update_user function here


# @api_view(['DELETE'])
# Write your delete_user function here
