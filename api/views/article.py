from rest_framework import viewsets
from api.serializers.article import *
from api.utils.wrapper import *
from django.contrib.contenttypes.models import ContentType
class ArticleView(viewsets.ModelViewSet):
    res = {'code': '1000', 'data': None}
    @exception_wrapper
    def list(self, request, *args, **kwargs):
        course_objs = models.Article.objects.all()
        sa = ArticleSerializers(course_objs, many=True)
        self.res['data'] = sa.data
        return Response(data=self.res)

    @exception_wrapper
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        article_obj = models.Article.objects.filter(pk=pk).first()
        sa = ArticleDetailSerializers(article_obj, many=False)
        self.res['data'] = sa.data
        return Response(data=self.res)


class CommentView(viewsets.ModelViewSet):
    res = {'code': '1000', 'data': None}

    @exception_wrapper
    def retrieve(self, request, *args, **kwargs):
        article_id = request.GET.get('article_id')
        content_type_id = ContentType.objects.filter(model='article').first().id
        comment_objs = models.Comment.objects.filter(object_id=article_id,content_type_id=content_type_id).all()
        cs = CommentSerializers(comment_objs, many=True)
        print('------------',cs)
        self.res['data'] = cs.data
        return Response(data=self.res)








