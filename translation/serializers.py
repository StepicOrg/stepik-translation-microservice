from rest_framework import serializers
from translation.models import TranslationStep


class TranslationStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationStep
        fields = ("stepik_id", "created_at", "updated_at", "lang", "text", "service_name")
        # TODO add complex serializer for lessons


class TranslatedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationStep
        fields = ("stepik_id", "created_at", "updated_at", "service_name")
