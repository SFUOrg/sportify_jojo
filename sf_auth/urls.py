from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import register_user, login_user, register_user_jwt, login_user_jwt, get_profile, update_profile

app_name = 'sf_auth'

urlpatterns = [
    # Telegram login (existing)
    path('telegram/', login_user, name='login'),
    
    # Registration and login API endpoints
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    
    # JWT-based registration and login
    path('register-jwt/', register_user_jwt, name='register_jwt'),
    path('login-jwt/', login_user_jwt, name='login_jwt'),
    
    # Profile endpoints
    path('profile/', get_profile, name='get_profile'),
    path('profile/update/', update_profile, name='update_profile'),
    
    # JWT token endpoints
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]