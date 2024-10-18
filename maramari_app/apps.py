from django.apps import AppConfig


class MaramariAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maramari_app'

    def ready(self):
        import maramari_app.signals  # noqa