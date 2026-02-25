from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserProfile


# ================= REGISTER =================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "phone_number",
            "password",
            "email",
            "username",   # fullname
            "role",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = UserProfile(**validated_data)
        user.set_password(password)
        user.save()

        return user


# ================= LOGIN =================
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone_number")
        password = attrs.get("password")

        user = authenticate(
            username=phone,   # USERNAME_FIELD = phone_number
            password=password
        )

        if not user:
            raise serializers.ValidationError("Phone yoki password xato")

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
        }