import collections

import requests
from django.conf import settings
from django.db import models

from api_controller.constants import RequestedObject
from .translation import TranslatedStep, TranslatedLesson, TranslatedCourse, StepSource, TranslatedStepSource


# :param: string
#  make text with encoded symbols (";", "&", "+", "%")
def encode_symbols(text):
    text = text.replace(";", "%3B")
    text = text.replace("&", "%26")
    text = text.replace("+", "%2B")
    text = text.replace("%", "%25")
    return text


# Strange commas appear in such situations:
# text "Blue, Sky, Orange" -> Yandex received text "Blue Sky, Orange" ->
# we got an array as input ["Blue", "Sky,", "Orange"]
#
# :param array of strings
# delete accidentally happened commas and articles
def clear_text(texts):
    new_texts = []
    for idx, text in enumerate(texts):
        if text.lower() in ["the", "a", "an"]:
            continue
        elif len(text.split()) == 1:
            new_texts.append(text.strip(','))
        else:
            new_texts.append(text)
    return new_texts


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

    # :param text: step's text in html format
    # :param lang: step's lang
    # :returns: translated text or None if translation failed
    def create_text_translation(self, text, payload=False, **kwargs):
        if text:
            final_url = self.obj.base_url
            params = ["?{0}={1}".format("key", self.api_key)]
            for name, value in kwargs.items():
                params.append("&{0}={1}".format(name, value))
            params.append("&{0}={1}".format("format", "html"))
            # if text is long html, &lang param isn't parsed properly
            if payload:
                if isinstance(text[0], tuple):
                    new_text = []
                    for text_pair in text:
                        new_text.extend(list(text_pair))
                    new_text = [encode_symbols(x) for x in new_text]
                    text = " ".join(new_text)
                    params.append("&{0}={1}".format("text", text))
                    response = requests.get(final_url + "".join(params)).json()
                    translated_texts = [x.strip() for x in response['text'][0].split(' ')]
                    translated_texts = clear_text(translated_texts)
                    ret = []
                    for i in range(0, len(translated_texts), 2):
                        ret.append((translated_texts[i], translated_texts[i + 1]))
                    return ret
                else:
                    text = [encode_symbols(x) for x in text]
                    text = " ".join(text)
                    params.append("&{0}={1}".format("text", text))
                    response = requests.get(final_url + "".join(params)).json()
                    translated_texts = [x.strip() for x in response['text'][0].split(' ')]

                    return clear_text(translated_texts)
            else:
                params.append("&{0}={1}".format("text", encode_symbols(text)))
                response = requests.get(final_url + "".join(params)).json()
                # we use response['text'][0] as response['text'] is an array always consisting of 1 element
                return " ".join(response['text'][0])
        return ""


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
            return steps.filter(lang=lang)  # if steps are None, return None

    def get_step_source_translation(self, pk, lang, **kwargs):
        step_sources = TranslatedStepSource.objects.filter(stepik_id=pk, service_name=self.service_name)
        if lang is None and step_sources:
            return step_sources
        elif lang is not None:
            return step_sources.filter(lang=lang)  # if step_sources are None, return None

    # :returns: TranslatedLesson queryset or None
    def get_lesson_translation(self, pk, **kwargs):
        lesson = TranslatedLesson.objects.filter(stepik_id=pk, service_name=self.service_name)
        return lesson if lesson else None

    # :returns TranslatedCourse queryset or None
    def get_course_translation(self, pk, **kwargs):
        course = TranslatedCourse.objects.filter(stepik_id=pk, service_name=self.service_name)
        return course if course else None

    # void function, which creates translation of all steps in lesson
    def create_lesson_translation(self, pk, ids, texts, lang):
        lesson = TranslatedLesson.objects.get(stepik_id=pk)
        for i, id in enumerate(ids):
            step = TranslatedStep.objects.filter(stepik_id=id, lang=lang).first()
            if step:
                step.lesson = lesson
                step.save()
            else:
                # don't send empty strings to translation
                translated_text = texts[i][0] if not texts[i][0] else self.create_text_translation(texts[i][0],
                                                                                                   lang=lang)
                TranslatedStep.objects.create(stepik_id=id, lang=lang, text=translated_text, lesson=lesson,
                                              service_name=self.service_name, stepik_update_date=texts[i][1])

    # :returns: translated source of step-source
    def create_step_source_translation(self, json, lang, source_type):
        if source_type == StepSource.CHOICE:
            options = json["options"]
            texts = [option["text"] for option in options]
            texts = self.create_text_translation(texts, True, lang=lang)
            for i in range(len(texts)):
                options[i]["text"] = texts[i]
            json["options"] = options
        elif source_type == StepSource.MATCHING:
            pairs = json["pairs"]
            texts = []
            for pair in pairs:
                texts.append((pair["first"], pair["second"]))
            texts = self.create_text_translation(texts, True, lang=lang)
            pairs = [collections.OrderedDict([('first', text[0]), ('second', text[1])]) for text in texts]
            json["pairs"] = pairs
        return json

    def create_step_source_dict(self, source, translated_options, source_type):
        dict = {}
        if source_type == StepSource.CHOICE:
            texts = [option["text"] for option in source["options"]]
            translated_texts = [option["text"] for option in translated_options["options"]]
            for i in range(len(texts)):
                dict[texts[i]] = translated_texts[i]
        elif source_type == StepSource.MATCHING:
            texts = []
            for pair in source["pairs"]:
                texts.extend([pair["first"], pair["second"]])
            translated_texts = []
            for pair in translated_options["pairs"]:
                translated_texts.extend([pair["first"], pair["second"]])
            for i in range(len(texts)):
                dict[texts[i]] = translated_texts[i]
        return dict

    # :returns: json of languages used in step's translation for obj_type instance
    def get_available_languages(self, pk, obj_type):
        steps = None
        if obj_type == RequestedObject.STEP:
            steps = TranslatedStep.objects.filter(stepik_id=pk, service_name=self.service_name)
        elif obj_type == RequestedObject.LESSON:
            lesson = TranslatedLesson.objects.filter(stepik_id=pk, service_name=self.service_name)
            if not lesson:
                return None
            steps = lesson.first().steps.all()
        elif obj_type == RequestedObject.LESSON:
            course = TranslatedLesson.objects.filter(stepik_id=pk, service_name=self.service_name)
            if not course:
                return None
            steps = []
            for lesson in course.lessons.all():
                steps.extend(lesson.steps.all())  # if queryset is empty, nothing happened
        if not steps:
            return None
        unique_languages = set()
        for step in steps:
            if step.lang not in unique_languages:
                unique_languages.add(step.lang)
        return list(unique_languages) if steps else None

    def get_translation_ratio(self, pk, obj_type, lang):
        if obj_type is RequestedObject.LESSON:
            try:
                lesson = TranslatedLesson.objects.get(stepik_id=pk)
            except TranslatedLesson.DoesNotExist:
                return 0
            translated = 0
            for step in lesson.steps.all():
                if step.lang == lang:
                    translated += 1
            try:
                return translated / lesson.steps_count
            except ZeroDivisionError:
                return 0
        elif obj_type is RequestedObject.COURSE:
            try:
                course = TranslatedCourse.objects.get(stepik_id=pk)
            except TranslatedCourse.DoesNotExist:
                return 0
            translated = 0
            for lesson in course.lessons.all():
                for step in lesson.steps.all():
                    if step.lang == lang:
                        translated += 1
            try:
                return translated / course.steps_count
            except TranslatedCourse.DoesNotExist:
                return 0
