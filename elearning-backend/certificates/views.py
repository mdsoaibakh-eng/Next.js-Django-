import uuid
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from courses.models import Enrollment
from .models import Certificate
from .serializers import CertificateSerializer


class CompleteCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")

        enrollment = Enrollment.objects.get(
            student=request.user,
            course_id=course_id
        )

        enrollment.completed = True
        enrollment.save()

        certificate, created = Certificate.objects.get_or_create(
            student=request.user,
            course=enrollment.course,
            defaults={
                "certificate_id": str(uuid.uuid4()).split("-")[0]
            }
        )

        serializer = CertificateSerializer(certificate)
        return Response(serializer.data)


class MyCertificatesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        certificates = Certificate.objects.filter(student=request.user)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)
