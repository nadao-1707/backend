from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from .models import User,Appointment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True},'id':{'read_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token payload
        token['email'] = user.email
        token['role'] = user.role
        return token


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'date', 'time', 'doctor','is_reserved','patient']
        extra_kwargs = {'id': {'read_only': True}}
