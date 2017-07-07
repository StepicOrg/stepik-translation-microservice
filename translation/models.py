from django.db import models

from api_controller.models import ApiController
from django.conf import settings
import requests
import json


# Abstract classes

class TranslationService(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    base_url = models.CharField()
    api_version = models.FloatField()
    translated_symbols = models.IntegerField()
    api_key = models.CharField()

    def get_lesson(self, pk, lang):
        pass

    def get_step(self, pk, lang, type):
        pass

    def get_available_languages(self):
        pass

    def get_translated_ratio(self, lang, type_object, type_object_id):
        pass

    def update_translated_text(pk, lang, type, new_text):
        pass

    def create_translated_text(pk, lang, type):
        pass


class Translation(models.Model):
    class Meta:
        abstract = True

    stepik_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lang = models.CharField(blank=False)
    text = models.CharField(blank=False)


class TranslationStep(Translation):
    pass


class YandexTranslator(models.Model):
    base_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    api_version = 1.5
    api_key = settings.YANDEX_API_KEY
    api_controller = models.ForeignKey(
        ApiController,
        on_delete=models.CASCADE,
        related_name="translation_services"
    )

    # @returns TranslationStep object
    def get_step(self, pk, text, **kwargs):
        if TranslationStep.objects.filter(pk=pk).exists():
            return TranslationStep.objects.filter(pk=pk)[0]
        else:
            final_url = self.base_url
            params = ["?{0}={1}".format("key", self.api_key), "&{0}={1}".format("text", text)]
            for name, value in kwargs.items():
                params.append("&{0}={1}".format(name, value))
            response = requests.get(final_url + "".join(params)).json()
            newly_translated_step = TranslationStep.objects.create(
                stepik_id=pk, lang=lang, text=response['text']
            )
            # TODO research if needed
            newly_translated_step.save()
            return newly_translated_step
    def get_available_language(self):
        all_steps = TranslationStep.objects.all()
        unique_languages = {}
        for step in all_steps:
            if step.lang not in unique_languages:
                unique_languages.add(step)
        response = json.dumps(list(unique_languages))
