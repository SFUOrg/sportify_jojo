from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date_time', 'created_at')
    list_filter = ('created_at', 'date_time')
    search_fields = ('title', 'organizer__username')
    filter_horizontal = ('participants',)