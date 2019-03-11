from django.test import TestCase

# Create your tests here.

import os
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Luffy1.settings")
    import django
    django.setup()
    from api import models
    from django.contrib.contenttypes.models import ContentType
    article_obj = models.Article.objects.filter(pk=1).first()
    # print(article_obj)
    model_id = ContentType.objects.filter(model='article').first().id
    print(model_id)
