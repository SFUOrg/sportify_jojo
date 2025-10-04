# sf_meetings/admin.py
from django.contrib import admin
from .models import SportCategory, Meeting


@admin.register(SportCategory)
class SportCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'profiles_count', 'meetings_count')
    search_fields = ('name',)
    prepopulated_fields = {'description': ('name',)}  # не обязательно, но можно убрать

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Описание (кратко)'

    def profiles_count(self, obj):
        # Считаем профили, где это — основной спорт
        return obj.main_sport_profiles.count()
    profiles_count.short_description = 'Профилей (основной спорт)'

    def meetings_count(self, obj):
        return obj.meetings.count()
    meetings_count.short_description = 'Встреч'


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'organizer', 'sport_category',
        'date_time', 'latitude', 'longitude', 'participants_count'
    )
    list_filter = ('sport_category', 'date_time', 'organizer')
    search_fields = ('title', 'organizer__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('participants',)
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'sport_category', 'date_time')
        }),
        ('Организатор и участники', {
            'fields': ('organizer', 'participants')
        }),
        ('Геолокация', {
            'fields': ('latitude', 'longitude'),
            'description': 'Координаты места проведения встречи'
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = 'Участников'