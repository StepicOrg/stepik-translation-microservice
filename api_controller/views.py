from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api_controller.models import ApiController
from translation.serializers import TranslationStepSerializer


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

        print(lang, service_name, pk)
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
