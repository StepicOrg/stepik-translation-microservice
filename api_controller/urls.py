from django.conf.urls import url

from api_controller.views import TranslatedStepViewSet, TranslatedLessonViewSet, AvailableLanguagesViewSet, \
    TranslationalRatioViewSet, TranslatedCourseViewSet, TranslatedStepSourceViewSet

steps_detail = TranslatedStepViewSet.as_view({
    "get": "retrieve",
    "post": "create",
    "put": "update"
})

steps_list = TranslatedStepViewSet.as_view({"get": "list"})

lesson_detail = TranslatedLessonViewSet.as_view({
    "get": "retrieve",
    "post": "create",
    "put": "update"
})

course_detail = TranslatedCourseViewSet.as_view({
    "get": "retrieve",
    "post": "create"
})

lesson_list = TranslatedLessonViewSet.as_view({"get": "list"})
languages_list = AvailableLanguagesViewSet.as_view({"get": "retrieve"})
ratio_detail = TranslationalRatioViewSet.as_view({"get": "retrieve"})
course_list = TranslatedCourseViewSet.as_view({"get": "list"})

step_source_detail = TranslatedStepSourceViewSet.as_view({
    "get": "retrieve",
    "post": "create",
    "put": "update"
})

step_source_list = TranslatedStepViewSet.as_view({"get": "list"})

urlpatterns = [
    url(r'^api/translation/steps/(?P<pk>[0-9]+)$', steps_detail, name="step-datail"),
    url(r'^api/translation/steps/$', steps_list, name="step-list"),
    url(r'^api/translation/lessons/(?P<pk>[0-9]+)$', lesson_detail, name="lesson-detail"),
    url(r'^api/translation/lessons/', lesson_list, name="lesson-list"),
    url(r'^api/translation/step-sources/(?P<pk>[0-9]+)$', step_source_detail, name="step-source-datail"),
    url(r'^api/translation/step-sources/$', step_source_list, name="step-source-list"),
    url(r'^api/translation/courses/(?P<pk>[0-9]+)$', course_detail, name="course-detail"),
    url(r'^api/translation/courses/', course_list, name="course-list"),
    url(r'^api/translational-ratio/(?P<obj_type>[a-z]+)/(?P<pk>[0-9]+)$', ratio_detail, name="translational_ratio"),
    url(r'^api/available-languages/(?P<obj_type>[a-z]+)/(?P<pk>[0-9]+)$', languages_list, name="available_languages"),
]
