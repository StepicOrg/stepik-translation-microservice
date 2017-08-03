from django.conf.urls import url

from api_controller.views import TranslatedStepViewSet, TranslatedLessonViewSet, AvailableLanguagesViewSet, \
    TranslationalRatioViewSet

steps_detail = TranslatedStepViewSet.as_view({
    "get": "retrieve",
    "post": "create",
    "put": "update"
})

steps_list = TranslatedLessonViewSet.as_view({"get": "list"})

lesson_detail = TranslatedLessonViewSet.as_view({
    "get": "retrieve",
    "post": "create",
    "put": "update"
})

lesson_list = TranslatedLessonViewSet.as_view({"get": "list"})

languages_list = AvailableLanguagesViewSet.as_view({"get": "retrieve"})

ratio_detail = TranslationalRatioViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    url(r'^api/translation/steps/(?P<pk>[0-9]+)$', steps_detail, name="step-datail"),
    url(r'^api/translation/steps/', steps_list, name="step-list"),
    url(r'^api/translation/lessons/(?P<pk>[0-9]+)$', lesson_detail, name="lesson-detail"),
    url(r'^api/translation/lessons/', lesson_list, name="lesson-list"),
    url(r'^api/translational_ratio/(?P<obj_type>[a-z]+)/(?P<pk>[0-9]+)$', ratio_detail, name="translational_ratio"),
    url(r'^api/available_languages/(?P<obj_type>[a-z]+)/(?P<pk>[0-9]+)$', languages_list, name="available_languages"),
]
