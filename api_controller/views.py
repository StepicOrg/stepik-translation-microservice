from django.shortcuts import render
# from translation.serializers import TranslationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translation.models import TranslationStep

class Translation(APIView):
    """
    Get translation of object_type with obj_id
    """
    def get(self, request, format=None):
        pass
