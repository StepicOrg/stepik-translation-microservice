from django.conf.urls import url
from api_controller import views

urlpatterns = [
    url(r'^api/translation/(?P<pk>[0-9]+)$', views.Translation.as_view(), name="translation"),
    #url(r'^api/translational_ratio', views.TranslationalRatio.as_view(), name="translational_ratio"),
    #url(r'^api/available_languages', views.AvailableLanguages.as_view(), name="available_languages"),
]