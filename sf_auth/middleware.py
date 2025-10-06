# myapp/exception_middleware.py (Пример, не универсальный)
from django.shortcuts import redirect
from django.contrib import messages
from social_core.exceptions import AuthAlreadyAssociated

class SocialAuthExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            # Добавляем сообщение об ошибке
            messages.error(request, "Этот аккаунт Telegram уже связан с другим пользователем.")
            # Перенаправляем на нужную страницу
            return redirect('profile_view') # или другую страницу
        return None # Возвращаем None, чтобы обработка продолжилась стандартно