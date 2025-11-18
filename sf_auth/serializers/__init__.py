from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.profile import Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('uuid', 'user', 'created_at', 'updated_at')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating profile, restricts certain fields that shouldn't be updated directly
    """
    class Meta:
        model = Profile
        fields = (
            'profile_photo', 'second_name', 'description', 'main_sport', 
            'latitude', 'longitude', 'find_area', 'birthday'
        )
        read_only_fields = ('uuid', 'user', 'created_at', 'updated_at', 'telegram_id')