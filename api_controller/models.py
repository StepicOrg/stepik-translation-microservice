from django.db import models
from django.conf import settings


class ApiController(models.Model):
    api_key = settings.STEPIK_API_KEY
    base_url = models.CharField()
    api_version = 0.1

    def get_translation(self, obj_type, service_name, pk, lang):
        translation_service = self.translation_services.filter(service_name=service_name)
        if obj_type == "lesson":
            result = translation_service.get_lesson(pk, lang)
        else:
            result = translation_service.get_step(pk, lang)
        # TODO make json serializer
        return result

    def get_available_languages(self, obj_type, service_name, pk):
        # TODO add obj_type "course"
        translational_service = self.translation_services.filter(service_name=service_name)
        if obj_type == "service":
            result = translational_service.get_available_languages()
        elif obj_type == "step":
            result = translational_service.filter(pk=pk)
        elif obj_type == "lesson":
            result = self.translation_services.filter(pk=pk)
        # TODO make json serializer
        return

    def get_translation_ratio(self, obj_type, pk):
        self.translation_service.get_translation_ratio(obj_type, )
