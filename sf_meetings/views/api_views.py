from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sf_meetings.models import Meeting
from sf_meetings.serializers import MeetingCreateSerializer, MeetingSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_meeting_api(request):
    """
    API endpoint to create a new meeting.
    Expects JSON data with fields: title, description, latitude, longitude, date_time, sport_category
    """
    serializer = MeetingCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        # Create meeting instance but don't save to database yet
        meeting = serializer.save()
        # Set the organizer to the current authenticated user
        meeting.organizer = request.user
        meeting.save()
        
        # Add the organizer as a participant (this is handled by the model's save method)
        
        # Return the complete meeting data with the newly assigned ID
        response_serializer = MeetingSerializer(meeting)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_meetings_api(request):
    """
    API endpoint to list meetings with optional filtering
    Query parameters:
    - sport_category: Filter by sport category ID
    - date_from: Filter meetings from this date (format: YYYY-MM-DD)
    - date_to: Filter meetings until this date (format: YYYY-MM-DD)
    - joined: If 'true', only show meetings the user has joined
    - organized: If 'true', only show meetings the user has organized
    """
    meetings = Meeting.objects.all()
    
    # Filter by sport category
    sport_category = request.query_params.get('sport_category')
    if sport_category:
        meetings = meetings.filter(sport_category_id=sport_category)
    
    # Filter by date range
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    
    if date_from:
        from datetime import datetime
        try:
            date_from_obj = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
            meetings = meetings.filter(date_time__gte=date_from_obj)
        except ValueError:
            return Response({'error': 'Invalid date_from format. Use YYYY-MM-DD.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    if date_to:
        from datetime import datetime
        try:
            date_to_obj = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
            meetings = meetings.filter(date_time__lte=date_to_obj)
        except ValueError:
            return Response({'error': 'Invalid date_to format. Use YYYY-MM-DD.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    # Filter by user participation
    joined = request.query_params.get('joined')
    if joined and joined.lower() == 'true':
        meetings = meetings.filter(participants=request.user)
    
    # Filter by user organization
    organized = request.query_params.get('organized')
    if organized and organized.lower() == 'true':
        meetings = meetings.filter(organizer=request.user)
    
    # Order by date_time
    meetings = meetings.order_by('date_time')
    
    serializer = MeetingSerializer(meetings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meeting_detail_api(request, pk):
    """
    API endpoint to get details of a specific meeting
    """
    try:
        meeting = Meeting.objects.get(pk=pk)
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)
    except Meeting.DoesNotExist:
        return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_meeting_api(request, pk):
    """
    API endpoint to delete a meeting
    Only the organizer can delete the meeting
    """
    try:
        meeting = Meeting.objects.get(pk=pk)
        
        # Check if the current user is the organizer
        if meeting.organizer != request.user:
            return Response({'error': 'You do not have permission to delete this meeting'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        meeting.delete()
        return Response({'message': 'Meeting deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)
    except Meeting.DoesNotExist:
        return Response({'error': 'Meeting not found'}, status=status.HTTP_404_NOT_FOUND)