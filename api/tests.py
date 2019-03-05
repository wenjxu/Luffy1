from django.test import TestCase

# Create your tests here.

import os
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Luffy1.settings")
    import django
    django.setup()
    from api import models
    course_objs = models.Course.objects.all()
