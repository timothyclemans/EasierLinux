from django.db import models
import sys
import urllib2
import json
import cookielib
import urllib

class Status(models.Model):
    step = models.PositiveIntegerField()
    running_status = models.CharField(max_length=30)

#    def __init__(self):
#        return '%s %s' % (self.step, self.running_status)
