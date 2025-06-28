from rest_framework import serializers
from .utils import send_welcome_email
from .models import BrandProfile, CustomAccounts, UserProfile
from django.contrib.auth import authenticate
from django.utils.cache import caches
from django.contrib.auth import get_user_model

User = get_user_model()
cache = caches['default']
#check knox loginview doc to recall why u need custom serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAccounts
        fields = ('first_name', 'last_name', 'email')
       

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAccounts
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        user = CustomAccounts(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        send_welcome_email(recipient_list= [user.email])
        return user
    


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserProfile
        fields = ('user', 'dob', 'phone_number', 'address', 'state', 'city', 'zip_code')
        


class BrandProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = BrandProfile
        fields = "__all__"


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials!")
    

#########################################################
class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
class ConfirmPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        code = cache.get(f"pwd_reset_{data['email']}")
        if code != data['code']:
            raise serializers.ValidationError("Invalid or expired code.")
        return data

    def save(self):
        user = User.objects.get(email=self.validated_data["email"])
        user.set_password(self.validated_data["new_password"])
        user.save()
        cache.delete(f"pwd_reset_{self.validated_data['email']}")

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
