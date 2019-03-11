from api import models
from rest_framework import serializers
class ArticleSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = "__all__"

class ArticleDetailSerializers(serializers.ModelSerializer):
    source = serializers.CharField(source='source.name')
    class Meta:
        model = models.Article
        fields = "__all__"

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"







