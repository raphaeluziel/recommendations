from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User

import time
from datetime import datetime

# Create your models here.


def generate_filename(self, filename):
    file_location = "%s/%s" % (self.student, filename)
    return file_location


class Responses(models.Model):
    STATUS_CHOICES = [
        ('Not Submitted', 'Not Submitted'),
        ('Submitted', 'Submitted'),
        ('Pending', 'Pending'),
        ('Written', 'Written')
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question01 = models.CharField(max_length=2500, default='', blank=True)
    question02 = models.CharField(max_length=2500, default='', blank=True)
    question03 = models.CharField(max_length=2500, default='', blank=True)
    question04 = models.CharField(max_length=2500, default='', blank=True)
    question05 = models.CharField(max_length=2500, default='', blank=True)
    question06 = models.CharField(max_length=2500, default='', blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not submitted')
    file_upload = models.FileField(upload_to=generate_filename, max_length=254, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.student)
