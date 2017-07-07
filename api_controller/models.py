from django.db import models
from django.conf import settings

class ApiController(models.Model):
    api_key = settings.STEPIK_API_KEY
    base_url = models.CharField()
    api_version = 0.1


