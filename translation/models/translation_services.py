from .translation import TranslationStep, TranslatedLesson
from django.db import models
from django.conf import settings

import requests
import json


class TranslationService(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service_name = models.CharField(max_length=40)
    base_url = models.CharField()
    api_version = models.FloatField()
    api_key = models.CharField()
    translated_symbols = models.IntegerField()
    count_steps = models.IntegerField()

    def get_step_translation(self, pk, lang, lesson):
        raise NotImplementedError

    def create_step_translation(self, pk, lang, type):
        raise NotImplementedError

    def update_step_translation(self, pk, lang, new_text):
        raise NotImplementedError

    def get_lesson_translated_steps(self, pk, lang):
        raise NotImplementedError

    def get_available_languages(self):
        raise NotImplementedError

    def get_translation_ratio(self, lang, type_object, type_object_id):
        pass


class YandexTranslator(TranslationService):
    base_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    service_name = "YANDEX"
    api_version = 1.5
    api_key = settings.YANDEX_API_KEY
    from api_controller.models import ApiController
    api_controller = models.ForeignKey(
        ApiController,
        on_delete=models.CASCADE,
        related_name="translation_services"
    )

    # :param pk: step's stepik_id
    # :param lang: step's lang
    # :returns: TranslationStep object or None
    def get_step_translation(self, pk, lang, **kwargs):
        # TODO can we optimize request?
        if TranslationStep.objects.filter(pk=pk, lang=lang).exists():
            return TranslationStep.objects.filter(pk=pk, lang=lang)[0]
        else:
            return None

    # :param pk: step's stepik_id
    # :param lang: step's lang
    # :param text: step's text in html format
    # :returns: TranslationStep object or None
    def create_step_translation(self, pk, lang, text, lesson, **kwargs):
        step = self.get_step(pk, lang)
        if step is None:
            final_url = self.base_url
            params = ["?{0}={1}".format("key", self.api_key), "&{0}={1}".format("text", text)]
            for name, value in kwargs.items():
                params.append("&{0}={1}".format(name, value))
            response = requests.get(final_url + "".join(params)).json()
            newly_translated_step = TranslationStep.objects.create(
                stepik_id=pk, lang=lang, text=response['text']
            )
            return newly_translated_step
        else:
            return step

    # :param pk: step's stepik_id
    # :param new_text: new translation of step's text
    # :param lang: step's lang
    # :returns: True or False
    def update_step_translation(self, pk, lang, new_text):
        if TranslationStep.objects.filter(pk=pk, lang=lang).exidsts():
            step = TranslationStep.objects.filter(pk=pk, lang=lang)[0]
        else:
            step = self.create_step_translation(pk, lang)
        step.text = new_text
        step.save()
        return True

    # :param pk: lesson's stepik_id
    # :param lang: step's lang
    # :returns: json of steps ids
    def get_lesson_translated_steps(self, pk, lang, **kwargs):
        if TranslatedLesson.objects.filter(pk=pk).exists():
            lesson = TranslatedLesson.objects.filter(pk=pk)[0]
        else:
            return None
        ids = []
        for step in lesson.steps:
            ids.append(step.pk)
        return json.dumps(ids)

    # :param pk: lesson's stepik_id
    # :param lang: step's lang
    # :returns: json of steps ids
    def translate_lesson(self, pk, lang):
        ids = self.get_lesson_translated_steps(pk, lang)
        if ids is not None:
            return ids
        else:
            # TODO implement Stepik API logic
            stepik_ids = [1, 2, 3]
            text = "gfadsf"
            ids = []
            for id in stepik_ids:
                step = self.create_step_translation(id, lang, text, pk)
                ids.append(step)
            return json.dumps(ids)

    # :returns: json of languages used in step's translation
    def get_available_languages(self):
        all_steps = TranslationStep.objects.filter(service_name=self.service_name)
        unique_languages = set()
        # http://blog.etianen.com/blog/2013/06/08/django-querysets/
        for step in all_steps.iterator():
            if step.lang not in unique_languages:
                unique_languages.add(step.lang)
        return json.dumps(list(unique_languages))

    def get_translation_ratio(self):
        pass
