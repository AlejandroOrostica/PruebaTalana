
from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from user.tasks import send_welcome_email_task

from user import models
from user import serializers
import random


# ____________________User views____________________

class UserList(APIView):
    """List all users, or create a new user."""

    def get_user_object(self, user_email):
        try:
            return get_user_model().objects.get(
                email=user_email
            )
        except models.User.DoesNotExist:
            return None

    def get(self, request, format=None):
        users = get_user_model().objects.all()
        serializer = serializers.UserListSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = serializers.UserPostSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            send_welcome_email_task.delay(
                name = user.name,
                email= user.email,
                subject = 'Bienvenido al sorteo ! ' 
            )

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ValidateEmail(APIView):

    def get_user(self, email):
        try:
            return get_user_model().objects.get(email=email)
        except models.User.DoesNotExist:
            raise Http404

    def get(self, request, email, format=None):


        user = self.get_user(email)

        
        if not user.is_active:
            user.is_active = True
            user.save()
            return Response({'Validated email ! '}, status=status.HTTP_200_OK)
        return Response({'Email already validated'}, status=status.HTTP_200_OK)


class PickWinner(APIView):
    
    def get(self, request, format=None):

        users = get_user_model().objects.filter(is_active = True)
        user = random.choice(users)
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)





        

class UserInfo(APIView):

    def get_user(self, pk):
        """Retrieve and return authenticated user"""
        try:
            return get_user_model().objects.get(pk=pk)
        except models.User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):

        user = self.get_user(pk)
        if user:
            serializer = serializers.UserDetailSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk, format=None):
        user = self.get_user(pk)
        if user:
            serializer = serializers.UserUpdateSerializer(user, data=request.data,
                                                          partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
