from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_name = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Certificate
        fields = "__all__"

    def get_student_name(self, obj):
        return obj.student.get_full_name() or obj.student.username
