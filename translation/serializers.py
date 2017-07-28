from rest_framework import serializers
from translation.models import TranslatedStep
from translation.models import TranslatedLesson


class TranslationStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslatedStep
        fields = ("pk", "stepik_id", "created_at", "updated_at", "lang", "text", "service_name")


class TranslatedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslatedLesson
        fields = ("stepik_id", "created_at", "updated_at", "service_name")
        steps = TranslationStepSerializer(many=True)
