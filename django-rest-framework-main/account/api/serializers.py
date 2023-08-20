from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, Serializer
from account.models import Profile
from rest_framework import serializers


class ProfileSerializer(ModelSerializer):
    #alta veriyoruz
    class Meta:
        model = Profile
        fields = ('id', 'about', 'address')

#update user information
class UserSerializer(ModelSerializer):
    #üstten aliyoruz
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'profile')

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        profile_serializer = ProfileSerializer(instance.profile, data=profile)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        return super(UserSerializer, self).update(instance, validated_data)

# changing password
class ChangePasswordSerializer(Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        #hazir func
        validate_password(value)
        return value

#register
class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def validate(self, attr):
        validate_password(attr['password'])
        return attr

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user