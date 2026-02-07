from django.urls import path
from .views import CreatePaymentIntentView, ConfirmPaymentView

urlpatterns = [
    path('create-intent/', CreatePaymentIntentView.as_view()),
    path('confirm/', ConfirmPaymentView.as_view()),
]
