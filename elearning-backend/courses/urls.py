from django.urls import path
from .views import (
    CourseCreateView,
    CourseListView,
    EnrollCourseView,
    TeacherCourseListView,
)

urlpatterns = [
    path('create/', CourseCreateView.as_view()),
    path('list/', CourseListView.as_view()),
    path('', CourseListView.as_view()),  # Handle /api/courses/
    path('teacher/my/', TeacherCourseListView.as_view()),
    path('enroll/', EnrollCourseView.as_view()),
]
