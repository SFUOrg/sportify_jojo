from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models.profile import Profile
from ..serializers import ProfileSerializer, ProfileUpdateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    API endpoint to get the current user's profile
    """
    try:
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response(
            {'error': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    API endpoint to update the current user's profile
    Only allows the user to update their own profile
    """
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return Response(
            {'error': 'Profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # Determine if it's a full update (PUT) or partial update (PATCH)
    partial = request.method == 'PATCH'
    
    serializer = ProfileUpdateSerializer(
        profile, 
        data=request.data, 
        partial=partial
    )
    
    if serializer.is_valid():
        serializer.save()
        # Return the full profile data after update
        full_serializer = ProfileSerializer(profile)
        return Response(full_serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)