# sf_auth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, ProfilePhoto


class ProfilePhotoInline(admin.TabularInline):
    model = ProfilePhoto
    extra = 1
    fields = ('image', 'is_main', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    show_change_link = True


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'uuid', 'telegram_id', 'second_name',
        'main_sport', 'birthday', 'created_at'
    )
    list_filter = ('main_sport', 'created_at', 'birthday')
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'second_name', 'telegram_id'
    )
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    inlines = [ProfilePhotoInline]
    fieldsets = (
        ('Пользователь', {
            'fields': ('user', 'uuid')
        }),
        ('Основная информация', {
            'fields': ('second_name', 'description', 'profile_photo', 'birthday')
        }),
        ('Спорт', {
            'fields': ('main_sport', 'sport_categories')
        }),
        ('Геолокация', {
            'fields': ('latitude', 'longitude', 'find_area'),
            'classes': ('collapse',)
        }),
        ('Telegram', {
            'fields': ('telegram_id',),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    filter_horizontal = ('sport_categories', 'meetings')


# Опционально: интеграция Profile в админку User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Отменяем регистрацию стандартного User и регистрируем с инлайном
admin.site.unregister(User)
admin.site.register(User, UserAdmin)