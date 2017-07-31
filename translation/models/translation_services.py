from .translation import TranslatedStep, TranslatedLesson
from django.db import models
from django.conf import settings
from api_controller.constants import RequestedObject

import requests
import json


class GoogleTranslator(object):
    def __init__(self, obj):
        self.obj = obj


class AzureTranslator(object):
    def __init__(self, obj):
        self.obj = obj


class YandexTranslator(object):
    def __init__(self, obj):
        self.obj = obj
        self.api_key = settings.YANDEX_API_KEY

    # :param pk: step's stepik_id
    # :param new_text: new translation of step's text
    # :param lang: step's lang
    # :returns: True or False
    def update_step_translation(self, pk, lang, new_text):
        qs = TranslatedStep.objects.filter(pk=pk, lang=lang)
        step = self.create_step_translation(new_text, lang=lang) if not qs else qs[0]
        step.text = new_text
        step.save()
        return True

    # :returns: json of languages used in step's translation
    def get_available_languages(self):
        all_steps = TranslatedStep.objects.filter(service_name=self.service_name)
        unique_languages = set()
        # http://blog.etianen.com/blog/2013/06/08/django-querysets/
        for step in all_steps.iterator():
            if step.lang not in unique_languages:
                unique_languages.add(step.lang)
        return json.dumps(list(unique_languages))

    def get_translation_ratio(self, pk, obj_type, lang):
        if obj_type is RequestedObject.LESSON:
            lesson = TranslatedLesson.objects.get(stepik_id=pk)
            translated = 0
            for step in lesson.step:
                if step.lang == lang:
                    translated += 1
            try:
                return translated / lesson.amount_steps
            except ZeroDivisionError:
                return 0


class TranslationService(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    service_name = models.CharField(max_length=40, unique=True)
    base_url = models.CharField(max_length=255)
    api_version = models.FloatField()
    translated_symbols = models.IntegerField(default=0)
    steps_count = models.IntegerField(default=0)

    api_controller = models.ForeignKey(
        'api_controller.ApiController',
        on_delete=models.PROTECT,
        related_name='translation_services',
        default=1
    )

    services = {
        'azure': AzureTranslator,
        'google': GoogleTranslator,
        'yandex': YandexTranslator,
    }

    @property
    def service(self):
        if not hasattr(self, '_service'):
            # create a new Service object and pass it this model instance
            self._service = self.services[self.service_name](self)
        return self._service

    def __getattr__(self, name):
        if name == '_service':
            raise AttributeError  # the service hasn't been instantiated yet
        # delegate all unknown lookups to the service object
        return getattr(self.service, name)

    # :param pk: step's stepik_id
    # :param lang: step's lang
    # :returns: TranslatedStep queryset or None
    def get_step_translation(self, pk, lang, **kwargs):
        steps = TranslatedStep.objects.filter(stepik_id=pk, service_name=self.service_name)
        if lang is None and steps:
            return steps
        elif lang is not None:
            return steps.filter(lang=lang)
        else:
            return None

    def get_lesson_translation(self, pk, **kwargs):
        lesson = TranslatedLesson.objects.filter(stepik_id=pk, service_name=self.service_name)
        return lesson if lesson else None

    # :param text: step's text in html format
    # :param lang: step's lang
    # :returns: translated text or None if translation failed
    def create_text_translation(self, text, **kwargs):
        # TODO problem with access
        final_url = self.base_url
        params = ["?{0}={1}".format("key", self.api_key), "&{0}={1}".format("text", text)]
        for name, value in kwargs.items():
            params.append("&{0}={1}".format(name, value))
        response = requests.get(final_url + "".join(params)).json()
        return response['text']

    def create_lesson_translation(self, pk, ids, texts, lang):
        lesson = TranslatedLesson.objects.get(stepik_id=pk)
        for id, i in enumerate(ids):
            step = TranslatedStep.objects.filter(stepik_id=id, lang=lang)
            if step:
                step.lesson = lesson
                step.save()
            else:
                # don't send empty strings to translation
                translated_text = texts[i] if not texts[i] else self.create_text_translation(texts[i][0], lang=lang)
                TranslatedStep.objects.create(stepik_id=id, lang=lang, text=translated_text, lesson=lesson,
                                              service_name=self.service_name, stepik_update_date=texts[i][1])
