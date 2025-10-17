from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Meeting
from django.contrib.auth.models import User


class JoinMeetingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        meeting_id = request.data.get('meeting_id')
        if not meeting_id:
            return Response(
                {'error': 'ID встречи обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            meeting = Meeting.objects.get(meeting_id=meeting_id)
        except Meeting.DoesNotExist:
            return Response(
                {'error': 'Встреча не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, не является ли пользователь уже участником
        if meeting.participants.filter(id=request.user.id).exists():
            return Response(
                {'message': 'Вы уже присоединены к этой встрече'}, 
                status=status.HTTP_200_OK
            )

        # Добавляем пользователя к участникам встречи
        meeting.participants.add(request.user)

        return Response({
            'message': f'Успешно присоединились к встрече {meeting_id}',
            'meeting_title': meeting.title
        }, status=status.HTTP_200_OK)


class LeaveMeetingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        meeting_id = request.data.get('meeting_id')
        if not meeting_id:
            return Response(
                {'error': 'ID встречи обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            meeting = Meeting.objects.get(meeting_id=meeting_id)
        except Meeting.DoesNotExist:
            return Response(
                {'error': 'Встреча не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Удаляем пользователя из участников встречи
        meeting.participants.remove(request.user)

        return Response({
            'message': f'Успешно покинули встречу {meeting_id}'
        }, status=status.HTTP_200_OK)