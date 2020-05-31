from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.

def generate_filename(self, filename):
    file_location = "%s/%s" % (self.student, filename)
    return file_location

class Responses(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question01 = models.CharField(max_length=2500, default='')
    question02 = models.CharField(max_length=2500, default='')
    question03 = models.CharField(max_length=2500, default='')
    question04 = models.CharField(max_length=2500, default='')
    question05 = models.CharField(max_length=2500, default='')
    question06 = models.CharField(max_length=2500, default='')
    file_upload = models.FileField(upload_to=generate_filename, max_length=254, null=True, blank=True)

    def __str__(self):
        # The top return is for older versions, like on my server
        return "{}\n{}".format(self.question01, self.question02)
