from django.apps import AppConfig

class UsageLimitsConfig(AppConfig):

    name = "usage_limits"

    def ready(self):
        import usage_limits.signals