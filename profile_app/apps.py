from django.apps import AppConfig

class ProfileAppConfig(AppConfig):
    name = 'profile_app'

    def ready(self):
        # hier nur das Signal-Modul laden, nicht umgekehrt
        import profile_app.api.signals