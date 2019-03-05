from django.test import TestCase

# Create your tests here.

rate = '3/m'
num, period = rate.split('/')
print(period[0])
