from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers



# ____________________Nested objects serializers____________________



class UserListSerializer(serializers.ModelSerializer):
    """Serializes a user object for listing them all"""


    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'rut',
            'email',
            'name',
            'last_name'
        )


class UserPostSerializer(serializers.ModelSerializer):
    """Serializes a user object for post, put and patch methods"""
    
    

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'rut',
            'password',
            'name',
            'last_name',
            'telephone',

        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                },
                'min_length': 6,
            }
        }

    def create(self, validated_data):
        """Create and  return  new user"""
        
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializes a user object for post, put and patch methods"""

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'password',
            'rut',
            'is_active',
            'name',
            'last_name',
            'telephone',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                },
                'min_length': 6,
            }
        }

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)  # remove the password

   
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializes a user object"""

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'name',
            'rut',
            'last_name',
            'telephone',
            'is_active',
        )