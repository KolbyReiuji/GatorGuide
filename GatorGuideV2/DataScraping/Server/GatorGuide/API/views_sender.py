from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import UserSerializer
from .models import User
# Create your views here.

# Write your bunch of GET function here
@api_view(['GET'])
def get_users(request):
    return Response(UserSerializer(User.objects.all(), many=True).data)
