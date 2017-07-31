from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Translation(models.Model):
    class Meta:
        abstract = True
        ordering = ["stepik_id"]

    stepik_id = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    stepik_update_date = models.DateTimeField(blank=False)
    lang = models.CharField(max_length=10, blank=False)
    text = models.TextField(blank=False)
    service_name = models.CharField(max_length=40)


class TranslatedLesson(models.Model):
    stepik_id = models.IntegerField(unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    stepik_update_date = models.DateTimeField(blank=False)
    service_name = models.CharField(max_length=40)
    steps_count = models.IntegerField(default=0)

    def get_languages(self):
        unique_languages = set()
        for step in self.steps.all():
            unique_languages.add(step.lang)
        return unique_languages


class TranslatedStep(Translation):
    lesson = models.ForeignKey(TranslatedLesson, on_delete=models.PROTECT, related_name="steps")


@receiver(post_save, sender=TranslatedStep, dispatch_uid="update_lesson_date")
def update_lesson_date(sender, instance, **kwargs):
    qs = TranslatedLesson.objects.filter(id=instance.lesson.pk)
    qs.update(update_date=instance.update_date)
