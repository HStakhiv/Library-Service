from django.apps import AppConfig


class BorrowingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrowing"

    def ready(self):
        from jobs import updater
        updater.start()
