from django.apps import AppConfig


class SfAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sf_auth'

    def ready(self):
        import sf_auth.signals
