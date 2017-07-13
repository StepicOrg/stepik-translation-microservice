from django.db import models
from django.conf import settings
import requests

class ApiController(models.Model):
    api_key = 0
    oauth_credentials = {
        "client_id": settings.STEPIK_CLIENT_ID,
        "client_secret": settings.STEPIK_CLIENT_SECRET,
    }
    base_url = models.TextField()
    api_version = 0.1
    translation_name_dict = {
        "yandex": "YandexTranslator",
        "azure":  "AzureTranslator",
        "google": "GoogleTranslator",
    }
    api_host = "https://stepik.org/"
    token = None

    def stepik_ouath(self):
        auth = requests.auth.HTTPBasicAuth(self.oauth_credentials["client_id"], self.oauth_credentials["client_secret"])
        response = requests.post('https://stepik.org/oauth2/token/',
                                 data={'grant_type': 'client_credentials'},
                                 auth=auth)
        self.token = response.json().get('access_token', None)
        if not self.token:
            print('Unable to authorize with provided credentials')
            exit(1)

    def fetch_stepik_object(self, obj_class, obj_id):
        api_url = '{}/api/{}s/{}'.format(self.api_host, obj_class, obj_id)
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + self.token}).json()
        return response['{}s'.format(obj_class)][0]

    def fetch_stepik_step(self, pk):
        return self.fetch_stepik_object("step", pk)

    def fetch_stepik_lesson(self, pk):
        return self.fetch_stepik_object("lesson", pk)

    def get_translation(self, obj_type, service_name, pk, lang):
        service_class = self.translation_name_dict[service_name]
        translation_service = None
        for service in self.translation_services.all():
            # TODO replace eval
            if isinstance(service, eval(service_class)):
                translation_service = service
                break

        if obj_type == "lesson":
            result = translation_service.get_lesson(pk, lang)
        else:
            result = translation_service.get_step_translation(pk, lang)
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

        # def get_translation_ratio(self, obj_type, pk):
        #    self.translation_service.get_translation_ratio(obj_type, )
