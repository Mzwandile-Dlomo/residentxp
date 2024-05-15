from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # Ensure signals are imported when the app is ready
    def ready(self):
        from accounts.signals import set_user_permissions
