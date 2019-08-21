from django.test import TestCase
from .models import *
# Create your tests here.
print(Notice.objects.filter(pk=1))