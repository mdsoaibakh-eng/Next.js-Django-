from django.urls import path
from .views import (
    CourseCreateView,
    CourseListView,
    EnrollCourseView,
)

urlpatterns = [
    path('create/', CourseCreateView.as_view()),
    path('list/', CourseListView.as_view()),
    path('enroll/', EnrollCourseView.as_view()),
]
