import stripe
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.response import Response
from courses.models import Course, Enrollment
from .models import Payment
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = Course.objects.get(id=course_id)

        intent = stripe.PaymentIntent.create(
            amount=int(course.price * 100),
            currency="inr",
            metadata={
                "user_id": request.user.id,
                "course_id": course.id,
            },
        )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            stripe_payment_intent=intent["id"],
            amount=course.price,
            status="pending",
        )

        return Response({
            "client_secret": intent["client_secret"]
        })
class ConfirmPaymentView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        intent_id = request.data.get("payment_intent")

        payment = Payment.objects.get(
            stripe_payment_intent=intent_id,
            user=request.user
        )

        payment.status = "success"
        payment.save()

        Enrollment.objects.get_or_create(
            student=request.user,
            course=payment.course
        )

        return Response({"message": "Payment successful, enrolled!"})
