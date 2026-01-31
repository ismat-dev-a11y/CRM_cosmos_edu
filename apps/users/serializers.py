from rest_framework import serializers
from .models import UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializers(serializers.ModelSerializer):
  password = serializers.CharField(
        write_only=True,
        min_length=6
    )

  class Meta:
    model = UserProfile
    fields = ['username', 'phone_number', 'email', 'role', 'parent', 'password']
    read_only_fields = ['id', 'role']

  def create(self, validated_data):
    password = validated_data.pop('password')
    user = UserProfile.objects.create_user(password=password, **validated_data)
    return user


class UserVerifyLoginSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        attrs['username'] = attrs.get('phone_number')
        return super().validate(attrs)