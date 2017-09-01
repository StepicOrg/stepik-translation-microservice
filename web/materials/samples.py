"""
In this tutorial I show how to get objects from Translation API Microservice.
For post/put-requests and for attempts you need tokens. Please write me on maxim.averin@stepik.org
and I will give you them.
"""
import requests
import json

BASE_URL = "http://52.174.33.220:443/api/"

# Get step
step = requests.get("http://52.174.33.220:443/api/translation/steps/20957?service_name=yandex&lang=en")
print(step.text)
"""
{
    "meta": {
        "page": 1,
        "has_next": false,
        "has_previous": false
    },
    "steps": [
        {
            "pk": 2,
            "stepik_id": 20957,
            "create_date": "2017-09-01T08:57:20.607334Z",
            "update_date": "2017-09-01T08:57:20.607382Z",
            "stepik_update_date": "2015-02-21T10:19:53Z",
            "lang": "en",
            "text": "<h2>Welcome!</h2><p>We are glad to see you on the course \"Fundamentals of statistics\". In this introductory lesson, we will tell you about what is waiting for you, and give advice on the course. Press \"right\" button to move to the next step.</p><p>All slides of this week is available for downloading in PDF format <a href=\"/media/attachments/lesson/8095/%D0%A1%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0%20-%20%D0%9D%D0%B5%D0%B4%D0%B5%D0%BB%D1%8F%20%E2%84%961.pdf\">at this link</a>.</p><p></p>",
            "service_name": "yandex",
            "position": 1
        }
    ]
"""
# Get lesson
lesson = requests.get("http://52.174.33.220:443/api/translation/lessons/8095?service_name=yandex&lang=en")
json_dict = json.loads(lesson.text)
for step in json_dict["lessons"]:
    print(step)

# Get attempts and step-source

# Get statistics. List of langs, which are supported for current object
r = requests.get("http://52.174.33.220:443/api/available-languages/lessons/8095?service_name=yandex")
json_dict = json.loads(r.text)
for lang in json_dict["available_languages"]:
    print(lang)

# Get percent translation of current translation
r = requests.get("http://52.174.33.220:443/api/translational-ratio/lessons/8095?service_name=yandex&lang=en")
json_dict = json.loads(r.text)
print(json_dict["translational-ratio"]) # all steps of lesson are translated in english


# Try post methods. They are the same as get, but you have to do them with admin token
lesson = requests.post("http://52.174.33.220:443/api/translation/lessons/37853?service_name=yandex&lang=en&access_token=<put yours here>")

# If you want to get attempts, request it with stepik_token
attempt = requests.get("http://52.174.33.220:443/api/translation/attempts/24917428?service_name=yandex&lang=en&access_token=<put yours here>")


# If you try to requests some bad link, you will get {"detail":"Not found"}
not_found = requests.get("http://52.174.33.220:443/api/translation/")
print(not_found.status_code) # 404
