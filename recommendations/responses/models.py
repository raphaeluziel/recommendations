from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.

class Responses(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question01 = models.CharField(max_length=2500, default='Not Answered')
    question02 = models.CharField(max_length=2500, default='Not Answered')
    question03 = models.CharField(max_length=2500, default='Not Answered')
    question04 = models.CharField(max_length=2500, default='Not Answered')
    question05 = models.CharField(max_length=2500, default='Not Answered')
    question06 = models.CharField(max_length=2500, default='Not Answered')

    def __str__(self):
        # The top return is for older versions, like on my server
        return "{}\n{}".format(self.question01, self.question02)
