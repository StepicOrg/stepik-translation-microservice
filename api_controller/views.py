import collections

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from api_controller.models import ApiController
from api_controller.serializers import PaginationDecorator
from translation.models import TranslatedStep, TranslatedLesson
from translation.serializers import TranslatedStepSerializer, TranslatedLessonSerializer, TranslatedCourseSerializer
from .constants import RequestedObject


class BasicApiViewSet(viewsets.GenericViewSet):
    serializer_class = None
    paginate_by = 20  # how many objs for displaying on 1 page

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

    def get_serializer(self, instance=None, many=False, context=None, data=None):
        base_serializer = self.serializer_class(instance=instance, many=True, context=context)
        paginator = Paginator(base_serializer.data, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            objs = paginator.page(page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)

        final_objs = collections.OrderedDict({
            "page": objs,
            "type": self.get_type_object().value
        })
        return PaginationDecorator(final_objs)

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

        if not self.check_required_params(params):
            return self.error_response(404)

        obj = api_controller.create_translation(self.get_type_object(), params["pk"], params["service_name"],
                                                params["lang"])
        if obj is None:
            return self.error_response(404)
        serializer = self.get_serializer(instance=obj, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = self.get_queryset()
        if obj is not None:
            serializer = self.get_serializer(instance=obj, many=True)
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

    def check_required_params(self, params):
        for k, v in params.items():
            if not v and k is not "obj_type":
                return False
        return True


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

    def update(self, request, pk, **kwargs):
        params = self.get_params()
        params["text"] = self.request.query_params.get("text", None)
        api_controller = ApiController.load()

        if not self.check_required_params(params):
            return self.error_response(404)

        data = api_controller.update_translation(self.get_type_object(), params["pk"], params["text"],
                                                 params["service_name"], params["lang"])
        if data is None:
            return self.error_response(404)
        serializer = self.get_serializer(instance=data, many=True)
        return Response(serializer.data)


class TranslatedLessonViewSet(BasicApiViewSet):
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
        serializer = self.get_serializer(instance=obj, many=True, context={"lang": self.get_params()["lang"]})
        return Response(serializer.data)


class TranslationalRatioViewSet(BasicApiViewSet):
    serializer_class = serializers.FloatField

    def get_record(self, **kwargs):
        api_controller = ApiController.load()
        return api_controller.get_translational_ratio(kwargs["pk"], kwargs["obj_type"], kwargs["lang"],
                                                      kwargs["service_name"])

    def retrieve(self, request, obj_type=None, pk=None):
        obj = self.get_queryset()
        if obj is None:
            return self.error_response(404)
        meta = collections.OrderedDict([
            ('page', 1),
            ('has_next', False),
            ('has_previous', False),
        ])
        ret = collections.OrderedDict(meta=meta)
        ret["translational_ratio"] = obj
        return Response(ret)


class AvailableLanguagesViewSet(BasicApiViewSet):
    def get_record(self, **kwargs):
        api_controller = ApiController.load()
        return api_controller.get_available_languages(kwargs["pk"], kwargs["obj_type"], kwargs["service_name"])

    def retrieve(self, request, obj_type=None, pk=None):
        obj = self.get_queryset()
        if not isinstance(obj, list):
            obj = [obj]
        if obj is None:
            return self.error_response(404)
        meta = collections.OrderedDict([
            ('page', 1),
            ('has_next', False),
            ('has_previous', False),
        ])
        ret = collections.OrderedDict(meta=meta)
        ret["available_languages"] = obj
        return Response(ret)


class TranslatedCourseViewSet(BasicApiViewSet):
    serializer_class = TranslatedCourseSerializer

    def get_type_object(self):
        return RequestedObject.COURSE
