from django.db import models
from django.conf import settings
from translation.models import TranslatedLesson, TranslatedStep
from django.core.cache import cache
from datetime import datetime

from .constants import RequestedObject

import requests


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            object, created = cls.objects.get_or_create(pk=1)
            if not created:
                object.set_cache()
        return cache.get(cls.__name__)


class ApiController(SingletonModel):
    oauth_credentials = {
        "client_id": settings.STEPIK_CLIENT_ID,
        "client_secret": settings.STEPIK_CLIENT_SECRET,
    }
    api_version = models.FloatField(default=0.1)
    api_host = models.CharField(max_length=255, default="https://stepik.org")
    token = None

    def from_str_to_datetime(self, str):
        return datetime.strptime(str, "%Y-%m-%dT%H:%M:%SZ")

    def stepik_oauth(self):

        auth = requests.auth.HTTPBasicAuth(self.oauth_credentials["client_id"], self.oauth_credentials["client_secret"])
        response = requests.post('https://stepik.org/oauth2/token/',
                                 data={'grant_type': 'client_credentials'},
                                 auth=auth)
        self.token = response.json().get('access_token', None)
        if not self.token:
            return False
        return True

    # :returns stepik_object or None if any errors occured during call STEPIK API
    def fetch_stepik_object(self, obj_class, obj_id):
        api_url = '{}/api/{}s/{}'.format(self.api_host, obj_class, obj_id)
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + self.token}).json()
        if '{}s'.format(obj_class) in response:
            return response['{}s'.format(obj_class)][0]
        return None

    def fetch_stepik_objects(self, obj_class, obj_ids, keep_order=True):
        objs = []
        load_size = 30  # don't wanna hit HTTP request limits
        for i in range(0, len(obj_ids), load_size):
            slice = obj_ids[i:i + load_size]
            api_url = '{}/api/{}s/?{}'.format(self.api_host, obj_class, "&".join("ids[]={}".format(x) for x in slice))
            response = requests.get(api_url,
                                    headers={'Authorization': 'Bearer ' + self.token}).json()
            objs += response['{}s'.format(obj_class)]
        if keep_order:
            return sorted(objs, key=lambda x: obj_ids.index(x['id']))
        return objs

    def fetch_stepik_step(self, pk):
        return self.fetch_stepik_object("step", pk)

    def fetch_stepik_lesson(self, pk):
        return self.fetch_stepik_object("lesson", pk)

    # :returns: list of tuples(text, update_date)
    def steps_text_with_dates(self, ids):
        texts = []
        steps = self.fetch_stepik_objects("step", ids)
        for step in steps:
            if step is None or 'text' not in step['block']:
                texts.append("")
            else:
                texts.append((step['block']['text'], self.from_str_to_datetime(step['update_date'])))
        return texts

    # :returns: queryset with created translation object or None if service_name is None or can't be parsed or
    # if Stepik API returned 404 or have no permission
    def create_translation(self, obj_type, pk, service_name=None, lang=None):
        translation_service = self.get_service(service_name)
        if not translation_service:
            return None

        if obj_type is RequestedObject.STEP:

            translation = self.get_translation(obj_type, pk, service_name, lang)
            if translation is not None:
                return translation
            created = self.fetch_stepik_object(obj_type.value, pk)
            if created is None:
                return None
            created_step, lesson_keeper = None, None
            lesson = self.fetch_stepik_object("lesson", created['lesson'])
            translated_text = translation_service.create_text_translation(created['block']['text'], lang=lang)
            datetime_obj = self.from_str_to_datetime(lesson['update_date'])
            if TranslatedLesson.objects.filter(stepik_id=lesson["id"]).exists():
                lesson_keeper = TranslatedLesson.objects.filter(stepik_id=lesson["id"]).first()
            else:
                lesson_keeper = TranslatedLesson.objects.create(stepik_id=created['lesson'], service_name=service_name,
                                                                stepik_update_date=datetime_obj,
                                                                steps_count=len(lesson["steps"]))
            datetime_obj = self.from_str_to_datetime(created['update_date'])
            created_step = TranslatedStep.objects.create(stepik_id=pk, lang=lang, service_name=service_name,
                                                         text=translated_text,
                                                         stepik_update_date=datetime_obj,
                                                         lesson=lesson_keeper, position=created['position'])
            return TranslatedStep.objects.filter(pk=created_step.pk)
        elif obj_type is RequestedObject.LESSON:
            translation = self.get_translation(obj_type, pk, service_name, lang)
            # second cond. if we have already translated lesson's steps to lang
            if translation is not None and translation.first().steps.filter(
                    lang=lang).count() == translation.first().steps_count:
                return translation

            stepik_lesson = self.fetch_stepik_object(obj_type.value, pk)
            if stepik_lesson is None:
                return None

            lesson = None
            # if lesson already exists, but we didn't translate all steps
            if translation and translation.first().steps.filter(lang=lang).count() != translation.steps_count:
                lesson = translation
            else:
                datetime_obj = datetime.strptime(stepik_lesson['update_date'], "%Y-%m-%dT%H:%M:%SZ")
                lesson = TranslatedLesson.objects.create(stepik_id=pk, service_name=service_name,
                                                         stepik_update_date=datetime_obj,
                                                         steps_count=len(stepik_lesson["steps"]))

            texts = self.steps_text_with_dates(stepik_lesson['steps'])
            translation_service.create_lesson_translation(pk, stepik_lesson['steps'], texts, lang=lang)
            return TranslatedLesson.objects.filter(pk=lesson.pk)

    # :returns queryset translation or None if params are bad
    def get_translation(self, obj_type, pk, service_name=None, lang=None):

        result = None
        if service_name is None:
            if obj_type is RequestedObject.STEP:
                if lang is None:
                    result = TranslatedStep.objects.filter(stepik_id=pk)
                else:
                    result = TranslatedStep.objects.filter(stepik_id=pk, lang=lang)
            elif obj_type is RequestedObject.LESSON:
                if lang is None:
                    result = TranslatedLesson.objects.filter(stepik_id=pk)
                else:
                    result = TranslatedLesson.objects.filter(stepik_id=pk)
        else:
            translation_service = self.get_service(service_name)
            if not translation_service:
                return None
            if obj_type == RequestedObject.LESSON:
                result = translation_service.get_lesson_translation(pk)
            elif obj_type == RequestedObject.STEP:
                result = translation_service.get_step_translation(pk, lang)
        if result is None or result.exists() == 0:
            return None
        return result

    # :returns: queryset with one updated instance
    def update_translation(self, obj_type, pk, text=None, service_name=None, lang=None):
        if obj_type == RequestedObject.STEP:
            result = TranslatedStep.objects.filter(stepik_id=pk, service_name=service_name, lang=lang).first()
            if result:
                result.text = text
                result.save()
                return TranslatedStep.objects.filter(pk=result.pk)
        return None

    # :returns: list of languages in which stepik_object translation is available
    def get_available_languages(self, pk, obj_type, service_name):
        translation_service = self.get_service(service_name)
        if not translation_service:
            return None
        return translation_service.get_available_languages(pk, obj_type)

    # :returns: float percent indicating what part of stepik_object is translated in given language
    def get_translational_ratio(self, pk, obj_type, lang=None, service_name=None):
        translation_service = self.get_service(service_name)
        if not translation_service:
            return None
        return translation_service.get_translation_ratio(pk, obj_type, lang)

    # :returns TranslationService object or None if name isn't parsed or we haven't service with such name
    def get_service(self, service_name):
        if service_name is None:
            return None
        try:
            # convert queryset to object, yes it's guaranteed that service is the only one
            return self.translation_services.get(service_name=service_name.lower())
        except Exception:
            return None
