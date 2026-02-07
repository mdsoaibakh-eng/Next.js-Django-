from django.conf import settings
from django.db import models
from courses.models import Course

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('success', 'Success'),
            ('failed', 'Failed'),
        ),
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.course} - {self.status}"
