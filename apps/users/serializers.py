from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserProfile
from apps.groups.models import Group
from apps.enrollments.models import Enrollment
from django.db import transaction


# ================= REGISTER =================
from rest_framework import serializers
from django.db import transaction
from apps.users.models import UserProfile
from apps.courses.models import Course
from apps.enrollments.models import Enrollment
from apps.storedfiles.models import StoredFile

class RegisterSerializer(serializers.Serializer):
    fullName    = serializers.CharField()
    phone       = serializers.CharField()
    imgUrl      = serializers.PrimaryKeyRelatedField(
                    queryset=StoredFile.objects.all(),
                    required=False,
                    allow_null=True
                  )
    password    = serializers.CharField(write_only=True, min_length=6)
    courseId    = serializers.PrimaryKeyRelatedField(   # ← group emas, course!
                    queryset=Course.objects.filter(is_active=True),
                    required=False,
                    allow_null=True
                  )
    parentPhone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    parentName  = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_phone(self, value):
        if not value.startswith("+998") or len(value) != 13 or not value[1:].isdigit():
            raise serializers.ValidationError(
                "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak."
            )
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "Bu telefon raqam allaqachon ro'yxatdan o'tgan."
            )
        return value

    def validate_parentPhone(self, value):
        if value and (not value.startswith("+998") or len(value) != 13 or not value[1:].isdigit()):
            raise serializers.ValidationError(
                "Ota-ona telefon raqami +998XXXXXXXXX formatida bo'lishi kerak."
            )
        return value

    def validate(self, attrs):
        parent_phone = attrs.get('parentPhone')
        parent_name  = attrs.get('parentName')
        if bool(parent_phone) != bool(parent_name):
            raise serializers.ValidationError({
                "parentPhone": "parentPhone va parentName ikkalasi ham kiritilishi kerak."
            })
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        course       = validated_data.get('courseId')
        parent_phone = validated_data.get('parentPhone')
        parent_name  = validated_data.get('parentName')
        img_file     = validated_data.get('imgUrl')  # ← endi StoredFile objekti

        parent_instance = None
        if parent_phone and parent_name:
            parent_instance, created = UserProfile.objects.get_or_create(
                phone_number=parent_phone,
                defaults={
                    'username': parent_name,
                    'role'    : UserProfile.Role.PARENT,
                }
            )
            if created:
                parent_instance.set_password(parent_phone[-4:])
                parent_instance.save()

        student_user = UserProfile.objects.create_user(
        phone_number = validated_data['phone'],
        username     = validated_data['fullName'],
        password     = validated_data['password'],
        role         = UserProfile.Role.STUDENT,
        parent       = parent_instance,
        avatar       = validated_data.get('imgUrl'),
    )

        if course:
            Enrollment.objects.create(
                student   = student_user,
                course    = course,
                is_active = True,
                is_paid   = False,
            )

        return student_user


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
            username=phone,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Phone yoki password xato")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
        }

class UserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class StaffRegisterSerializer(serializers.Serializer):
    fullName = serializers.CharField()
    phone    = serializers.CharField()
    imgUrl   = serializers.PrimaryKeyRelatedField(   # ← FK
                   queryset=StoredFile.objects.all(),
                   required=False,
                   allow_null=True
               )
    password = serializers.CharField(write_only=True, min_length=6)
    role     = serializers.ChoiceField(choices=[
                   (UserProfile.Role.MENTOR, 'Mentor'),
                   (UserProfile.Role.BOSS,   'Super Admin'),
               ])

    def validate_phone(self, value):
        if not value.startswith("+998") or len(value) != 13 or not value[1:].isdigit():
            raise serializers.ValidationError(
                "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak."
            )
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "Bu telefon raqam allaqachon ro'yxatdan o'tgan."
            )
        return value

    def create(self, validated_data):
        img_file = validated_data.get('imgUrl')
        return UserProfile.objects.create_user(
            username     = validated_data['fullName'],
            phone_number = validated_data['phone'],
            password     = validated_data['password'],
            role         = validated_data['role'],
            avatar       = img_file,   # ← StoredFile FK
        )