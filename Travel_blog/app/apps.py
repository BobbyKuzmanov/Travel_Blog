from django.apps import AppConfig


class TravelAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Travel_blog.app'

    def ready(self):
        # Import and register signals
        import Travel_blog.app.signals
