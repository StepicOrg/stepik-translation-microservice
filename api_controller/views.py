from django.shortcuts import render
from translation.serializers import TranslationStepSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from translation.models import TranslationStep
from api_controller.models import ApiController
from rest_framework import generics
import json

#
# class Translation(generics.RetrieveAPIView):
#     """
#     Get translation of object_type with obj_id
#     """
#
#     def get_queryset(self):
#         if self.request.query_params.get("service_name"):
#             service_name = self.request.query_params.get("service_name")
#
#         if self.request.query_params.get("type"):
#             obj_type = self.request.query_params.get("type")
#
#         if self.request.query_params.get("lang"):
#             lang = self.request.query_params.get("lang")
#
#         print([obj_type, service_name, pk, lang])
#         ap = ApiController.objects.filter(id=1)[0]
#         step = ap.get_translation(obj_type, service_name, pk, lang)
#         serializer = TranslationStepSerializer(step)
#         return Response(serializer.data)

class Translation(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return TranslationStep.objects.get(pk=pk)
        except TranslationStep.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        step = self.get_object(pk)
        dict1 = {}
        dict1["detail"] = "Not found."
        if step is None:
            return Response({'please move along': 'nothing to see here'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TranslationStepSerializer(step)
        data = serializer.data
        if self.request.query_params.get("lang"):
            lang = self.request.query_params.get("lang")
            data["lang"] = lang
        return Response(data)
