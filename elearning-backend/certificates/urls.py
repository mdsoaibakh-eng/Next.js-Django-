from django.urls import path
from .views import CompleteCourseView, MyCertificatesView

urlpatterns = [
    path('complete/', CompleteCourseView.as_view()),
    path('my-certificates/', MyCertificatesView.as_view()),
]
