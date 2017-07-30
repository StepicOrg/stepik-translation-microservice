from rest_framework import serializers
from translation.models import TranslatedStep
from translation.models import TranslatedLesson


class TranslatedStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslatedStep
        fields = (
            "pk", "stepik_id", "create_date", "update_date", "stepik_update_date", "lang", "text", "service_name")


class TranslatedLessonSerializer(serializers.ModelSerializer):
    steps = TranslatedStepSerializer(many=True)

    class Meta:
        model = TranslatedLesson
        fields = (
        "stepik_id", "create_date", "update_date", "stepik_update_date", "service_name", "steps_count", "steps")
