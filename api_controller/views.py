from rest_framework.response import Response
from rest_framework import status
from api_controller.models import ApiController
from translation.serializers import TranslatedStepSerializer, TranslatedLessonSerializer
from translation.models import TranslatedStep, TranslatedLesson
import collections
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from .constants import RequestedObject
from rest_framework import viewsets
from api_controller.serializers import PaginationDecorator, SerializerTypeDataDecorator
from django.core.paginator import Page


class BasicApiViewSet(viewsets.GenericViewSet):
    serializer_class = None
    pagination_class = PageNumberPagination

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

    def get_serializer(self, instance=None, many=False, data=None):
        base_serializer = self.serializer_class(instance=instance, many=True)
        decorated_serializer = SerializerTypeDataDecorator(base_serializer, self.get_type_object())
        return PaginationDecorator(decorated_serializer)

    def list(self, request):
        objects = self.get_records()
        if objects is None:
            return self.error_response(404)
        serializer = self.get_serializer(instance=objects, many=True)
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
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = self.get_queryset()
        print("MASTER", obj)
        print(self.paginator)
        page = self.get_paginated_response(obj)
        print(page)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return Response(serializer.data)
        return self.error_response(404)

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
    pagination_class = PageNumberPagination
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
