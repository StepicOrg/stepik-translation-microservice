from django.db import models


class Translation(models.Model):
    class Meta:
        abstract = True

    stepik_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lang = models.CharField(max_length=10, blank=False)
    text = models.TextField(blank=False)
    service_name = models.CharField(max_length=40)


class TranslatedLesson(models.Model):
    stepik_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service_name = models.CharField(max_length=40)


class TranslationStep(Translation):
    lesson = models.ForeignKey(TranslatedLesson, on_delete=models.CASCADE, related_name="steps", blank=True)
