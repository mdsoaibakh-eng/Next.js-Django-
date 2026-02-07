import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import generics, permissions
from rest_framework.response import Response

from courses.models import Course
from enrollments.models import Enrollment
from .models import Payment

# Stripe config
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        intent = stripe.PaymentIntent.create(
            amount=int(course.price * 100),
            currency="inr",
            metadata={
                "user_id": request.user.id,
                "course_id": course.id,
            },
        )

        Payment.objects.create(
            user=request.user,
            course=course,
            stripe_payment_intent=intent.id,
            amount=course.price,
            status="pending",
        )

        return Response({
            "client_secret": intent.client_secret
        })


class ConfirmPaymentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        intent_id = request.data.get("payment_intent")

        payment = get_object_or_404(
            Payment,
            stripe_payment_intent=intent_id,
            user=request.user
        )

        # 🔒 Prevent duplicate processing
        if payment.status == "success":
            return Response({"message": "Already processed"})

        with transaction.atomic():
            payment.status = "success"
            payment.save()

            Enrollment.objects.get_or_create(
                student=request.user,
                course=payment.course
            )

        return Response({
            "message": "Payment successful, enrolled!"
        })
