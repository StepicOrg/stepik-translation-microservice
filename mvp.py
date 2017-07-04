import requests
import sys

YANDEX_API_KEY = "..."

client_id = "..."
client_secret = "..."
api_host = "https://stepik.org/"

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)


# get 1 json object
def fetch_object(obj_class, obj_id):
    api_url = '{}/api/{}s/{}'.format(api_host, obj_class, obj_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response['{}s'.format(obj_class)][0]


class YandexTranslator:
    base_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    api_key = YANDEX_API_KEY

    def get_translated_step(self, step_id, **kwargs):
        final_url = self.base_url
        step = fetch_object("step", step_id)
        final_url = ''.join([final_url, "?{0}={1}".format("key", self.api_key)])
        final_url = ''.join([final_url, "&{0}={1}".format("text", step["block"]["text"])])
        for name, value in kwargs.items():
           if name == "lang":
               final_url = ''.join([final_url, "&{0}={1}".format(name, value)])
           elif name == "format":
               final_url = ''.join([final_url, "&{0}={1}".format(name, value)])
        response = requests.get(final_url).json()
        return response['text']



step_id = 0
if len(sys.argv) == 2:
    step_id = sys.argv[1]
else:
    print("Error, enter course_id")
    exit(0)

translator = YandexTranslator()
print(translator.get_translated_step(step_id, lang="en", format="html"))
