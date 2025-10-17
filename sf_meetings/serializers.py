from rest_framework import serializers
from .models import Meeting
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class MeetingSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = ('meeting_id', 'title', 'description', 'latitude', 'longitude', 'date_time', 
                 'organizer', 'participants', 'sport_category', 'created_at', 'updated_at')
        read_only_fields = ('organizer', 'participants', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user
        meeting = Meeting.objects.create(organizer=user, **validated_data)
        # The organizer is automatically added as a participant in the model's save method
        return meeting


class MeetingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('meeting_id', 'title', 'description', 'latitude', 'longitude', 'date_time', 'sport_category')