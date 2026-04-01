# You may change these libraries depending on your use
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import UserSerializer
from .models import User
import uuid
from django.db import IntegrityError
# Create your views here.

# Write your create_user function here
@api_view(['POST'])
def create_user(request):
    UID = request.data.get('UID') or str(uuid.uuid4())
    serializer = UserSerializer(data=request.data)
    return createUser(serializer, UID)

# @api_view(['PUT'])
# Write your update_user function here
@api_view(['PUT'])
def update_user(request):
    UID = request.data.get('UID')
    if not UID:
        return Response({"errors":"User ID Not Found"}, status = status.HTTP_404_NOT_FOUND)
    return updateUser(UID, request.data)
   
# @api_view(['DELETE'])
# Write your delete_user function here
@api_view(['DELETE'])
def delete_user(request):
    UID = request.data.get('UID')

    if not UID:
        return Response({"errors":"User ID Not Found"}, status = status.HTTP_404_NOT_FOUND)
    return deleteUser(UID)
    

    


def createUser(serializer, UID):
    if User.objects.filter(user_id = UID).exists():
        return Response({"errors":"User Already Exists"}, status = status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        try:
            # Save using the `user_id` field (not the AutoField `id`)
            serializer.save(user_id=UID)
        except Exception as e:
            return Response({"errors":"Profile Created Failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Profile Created Successfully","data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"errors":"Profile Created Failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def updateUser(UID, data):
    try:
        user = User.objects.get(user_id=UID)
    except User.DoesNotExist:
        return Response({"errors":"User Not Found"}, status = status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, data=data, partial=True)
    try:
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Profile Updated Successfully", "data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"errors":"Profile Updated Failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"errors":"Update Failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def deleteUser(UID):
    try:
        deleted_count, _ = User.objects.filter(user_id=UID).delete()
        if deleted_count == 0:
            return Response({"errors":"User Not Found"}, status = status.HTTP_404_NOT_FOUND)
        return Response({"message":"Profile Deleted Successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"errors":"Delete Failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    