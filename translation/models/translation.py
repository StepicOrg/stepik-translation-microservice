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
    service_name = models.CharField(max_length=40)


class TranslatedCourse(Translation):
    steps_count = models.IntegerField(default=0)


class TranslatedLesson(Translation):
    steps_count = models.IntegerField(default=0)
    course = models.ForeignKey(TranslatedCourse, on_delete=models.SET_NULL, related_name="lessons", null=True)


class TranslatedStep(Translation):
    lang = models.CharField(max_length=10, blank=False)
    text = models.TextField(blank=False)
    position = models.IntegerField(default=1)
    lesson = models.ForeignKey(TranslatedLesson, on_delete=models.PROTECT, related_name="steps")


@receiver(post_save, sender=TranslatedStep, dispatch_uid="update_lesson_date")
def update_lesson_date(sender, instance, **kwargs):
    qs = TranslatedLesson.objects.filter(id=instance.lesson.pk)
    qs.update(update_date=instance.update_date)


@receiver(post_save, sender=TranslatedLesson, dispatch_uid="update_course_date")
def update_course_date(sender, instance, **kwargs):
    if instance.course is not None:
        qs = TranslatedCourse.objects.filter(id=instance.course.pk)
        qs.update(update_date=instance.update_date)
