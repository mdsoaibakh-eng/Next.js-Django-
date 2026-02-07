from django.conf import settings
from django.db import models
from courses.models import Course

User = settings.AUTH_USER_MODEL


class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.student} - {self.course}"
