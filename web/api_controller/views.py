import collections

from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from translation.models import TranslatedStep, TranslatedLesson
from translation.serializers import TranslatedStepSerializer, TranslatedLessonSerializer

from web.api_controller.models import ApiController
from .constants import RequestedObject


class BasicPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        has_next, has_previous = False, False
        if self.get_next_link():
            has_next = True
        if self.get_previous_link():
            has_previous = True

        meta = collections.OrderedDict([
            ('page', self.page.number),
            ('has_next', has_next),
            ('has_previous', has_previous),
        ])
        ret = collections.OrderedDict(meta=meta)
        ret["results"] = data
        return Response(ret)


class BasicApiViewSet(viewsets.GenericViewSet):
    serializer_class = None

    def get_queryset(self):
        params = self.get_params()
        data = self.get_record(**params)
        return data

    def get_params(self):
        params = dict()
        params["pk"] = self.kwargs.get("pk", None)
        try:
            params["obj_type"] = RequestedObject(self.kwargs["obj_type"][:-1])
        except KeyError:
            params["obj_type"] = None
        params["service_name"] = self.request.query_params.get("service_name", None)
        params["lang"] = self.request.query_params.get("lang", None)
        return params

    def get_type_object(self):
        raise NotImplementedError()

    def get_record(self, **kwargs):
        api_controller = ApiController.load()
        return api_controller.get_translation(self.get_type_object(), kwargs["pk"], kwargs["service_name"],
                                              kwargs["lang"])

    def get_records(self, **kwargs):
        pass

    def list(self, request):
        objects = self.get_records()
        if objects is None:
            return self.error_response(404)
        serializer = self.serializer_class(instance=objects, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        api_controller = ApiController.load()
        # TODO put it in another place
        api_controller.stepik_oauth()
        params = self.get_params()
        obj = api_controller.create_translation(self.get_type_object(), params["pk"], params["service_name"],
                                                params["lang"])

        if obj is None:
            return self.error_response(404)
        serializer = self.serializer_class(instance=obj)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = self.get_queryset()
        if obj is None:
            return self.error_response(404)
        serializer = self.serializer_class(instance=obj, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def error_response(self, number_error):
        if number_error == 404:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif number_error == 403:
            return Response({'detail': 'Action Forbidden.'}, status=status.HTTP_403_FORBIDDEN)

    def success_response(self, number_success):
        if number_success == 201:
            return Response({'detail': 'Successfully created.'}, status=status.HTTP_201_CREATED)
        elif number_success == 204:
            return Response({'detail': 'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)


class TranslatedStepViewSet(BasicApiViewSet):
    pagination_class = BasicPagination
    serializer_class = TranslatedStepSerializer

    def get_type_object(self):
        return RequestedObject.STEP

    def get_records(self, **kwargs):
        qs = TranslatedStep.objects.all()
        if "service_name" in self.request.query_params:
            qs = qs.filter(service_name=self.request.query_params["service_name"])
        if "lang" in self.request.query_params:
            qs = qs.filter(lang=self.request.query_params["lang"])
        return qs.order_by("pk")


class TranslatedLessonViewSet(BasicApiViewSet):
    pagination_class = BasicPagination
    serializer_class = TranslatedLessonSerializer

    def get_type_object(self):
        return RequestedObject.LESSON

    def get_records(self, **kwargs):
        qs = TranslatedLesson.objects.all()
        if "service_name" in self.request.query_params:
            qs = qs.filter(service_name=self.request.query_params["service_name"])
        return qs.order_by("pk")

    def retrieve(self, request, pk=None):
        obj = self.get_queryset()
        if obj is None:
            return self.error_response(404)
        serializer = self.serializer_class(instance=obj, many=True, context={"lang": self.get_params()["lang"]})
        return Response(serializer.data)


class TranslationalRatioViewSet(BasicApiViewSet):
    def get_record(self, **kwargs):
        api_controller = ApiController.load()
        return api_controller.get_translational_ratio(kwargs["pk"], kwargs["obj_type"], kwargs["lang"],
                                                      kwargs["service_name"])

    def retrieve(self, request, obj_type, pk=None):
        obj = self.get_queryset()
        if obj is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # serializer = serializers.FloatField(instance=obj)
            return Response(obj)


class AvailableLanguagesViewSet(BasicApiViewSet):
    def get_record(self, **kwargs):
        api_controller = ApiController.load()
        return api_controller.get_available_languages(kwargs["pk"], kwargs["obj_type"], kwargs["service_name"])

    def retrieve(self, request, obj_type, pk=None):
        obj = self.get_queryset()
        if obj is None:
            return self.error_response(404)
        return Response(obj)
