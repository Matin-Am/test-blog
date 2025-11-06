from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ...models import User,Profile
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255,write_only=True)
    class Meta:
        model = User
        fields = ["email","password","password1"]
        extra_kwargs = {
            "password":{"write_only":True}
        }

    def validate(self, attrs):
        p1 = attrs.get("password")
        p2 = attrs.get("password1")
        if p1 and p2 and p1 != p2:
            raise  serializers.ValidationError({"detail":"Passwords must match !"})
        try:
            password_validation.validate_password(password=p1)
        except ValidationError as e: 
            raise serializers.ValidationError({"password":list(e.messages)})
        return super().validate(attrs)


    def create(self, validated_data):
        validated_data.pop("password1")
        return User.objects.create_user(**validated_data)
    



class CustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({"detail":"User must be verified first!"})
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_verified:
                raise serializers.ValidationError("User must be verified first!")
        data["email"] = self.user.email
        data["user_id"] = self.user.pk
        return data


class ChangepasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, label="Old Password")
    new_password = serializers.CharField(min_length=8,label="New Password")
    confirm_password = serializers.CharField(min_length=8,label="Confirm Password")

    def validate(self, attrs):
        p1 = attrs.get("new_password")
        p2 = attrs.get("confirm_password")
        if p1 and p2 and p1 != p2:
            serializers.ValidationError("Passwords must match!")
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source="user.email")

    class Meta: 
        model = Profile
        fields = ("id","first_name","last_name","email","image","description")