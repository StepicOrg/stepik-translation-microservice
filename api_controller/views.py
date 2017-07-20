from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api_controller.models import ApiController
from translation.serializers import TranslationStepSerializer
from translation.models import TranslationStep
import collections
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination


class Translation(APIView):
    """
    Translate lesson or step from Stepik
    """

    def get(self, request, obj_type, pk, format=None):
        api_controller = ApiController.objects.filter(id=1)[0]
        service_name, lang = None, None

        if self.request.query_params.get("service_name"):
            service_name = self.request.query_params.get("service_name")
        if self.request.query_params.get("lang"):
            lang = self.request.query_params.get("lang")

        data = api_controller.get_translation(obj_type, pk, service_name, lang)

        if data is None:
            return self.error_response(404)
        else:
            if data.count() > 1:
                serializer = TranslationStepSerializer(list(data), many=True)
            else:
                serializer = TranslationStepSerializer(data[0])
            return Response(serializer.data)

    def error_response(self, number_error):
        if number_error == 404:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


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
        ret['results'] = data
        return Response(ret)


class Translations(ListAPIView):
    queryset = TranslationStep.objects.all()
    serializer_class = TranslationStepSerializer
    pagination_class = BasicPagination
