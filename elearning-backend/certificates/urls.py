from django.urls import path
from .views import CompleteCourseView, MyCertificatesView, CertificateDetailView

urlpatterns = [
    path('complete/', CompleteCourseView.as_view()),
    path('my-certificates/', MyCertificatesView.as_view()),
    path('<int:pk>/', CertificateDetailView.as_view()),
]
