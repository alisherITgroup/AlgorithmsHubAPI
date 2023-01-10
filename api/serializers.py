from .models import CodeSubmission, MathSubmission
from rest_framework import serializers
class CodeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSubmission
        fields = "__all__"
class MathSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MathSubmission
        fields = "__all__"