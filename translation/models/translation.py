from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    amount_steps = models.IntegerField(default=0)

    def get_languages(self):
        unique_languages = set()
        for step in self.steps.all():
            unique_languages.add(step.lang)
        return unique_languages


class TranslationStep(Translation):
    lesson = models.ForeignKey(TranslatedLesson, on_delete=models.CASCADE, related_name="steps")


@receiver(post_save, sender=TranslationStep, dispatch_uid="update_lesson_date")
def update_lesson_date(sender, instance, **kwargs):
    qs = TranslatedLesson.objects.filter(id=instance.lesson.pk)
    qs.update(updated_at=instance.updated_at)
