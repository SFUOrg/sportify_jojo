# meetings/forms.py
from django import forms
from .models import Meeting, SportCategory # Предполагаем, что модель SportCategory существует

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'description', 'latitude', 'longitude', 'date_time', 'sport_category'] # Исключаем organizer и participants
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Название мероприятия',
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#e0e0e0] bg-white focus:border-[#e0e0e0] h-14 placeholder:text-[#757575] p-[15px] text-base font-normal leading-normal'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Описание',
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#e0e0e0] bg-white focus:border-[#e0e0e0] min-h-36 placeholder:text-[#757575] p-[15px] text-base font-normal leading-normal'
            }),
            'latitude': forms.NumberInput(attrs={
                'placeholder': 'Широта (например, 55.7558)',
                'step': 'any', # Для точности координат
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#e0e0e0] bg-white focus:border-[#e0e0e0] h-14 placeholder:text-[#757575] p-[15px] text-base font-normal leading-normal'
            }),
            'longitude': forms.NumberInput(attrs={
                'placeholder': 'Долгота (например, 37.6176)',
                'step': 'any',
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#e0e0e0] bg-white focus:border-[#e0e0e0] h-14 placeholder:text-[#757575] p-[15px] text-base font-normal leading-normal'
            }),
            'date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local', # HTML5 input для даты и времени
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#e0e0e0] bg-white focus:border-[#e0e0e0] h-14 placeholder:text-[#757575] p-[15px] text-base font-normal leading-normal'
            }),
            'sport_category': forms.Select(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#e0e0e0] bg-white focus:border-[#e0e0e0] h-14 bg-[image:--select-button-svg] placeholder:text-[#757575] p-[15px] text-base font-normal leading-normal'
            }),
        }

    def __init__(self, *args, **kwargs):
        # Если вы хотите ограничить выбор категорий спорта, можно модифицировать queryset здесь
        super().__init__(*args, **kwargs)
        # Пример: self.fields['sport_category'].queryset = SportCategory.objects.filter(active=True)