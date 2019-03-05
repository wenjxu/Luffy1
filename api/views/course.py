from api import models
from rest_framework import viewsets
from rest_framework.views import Response
from api.serializers.course import CourseSerializer,CourseDetailSerializer
class CourseView(viewsets.ModelViewSet):

    queryset = models.Course.objects.all()

    serializer_class = CourseSerializer

    def retrieve(self, request, *args, **kwargs):

        pk =kwargs.get('pk')

        course_detail_obj = models.CourseDetail.objects.filter(pk=pk).first()

        cs = CourseDetailSerializer(course_detail_obj)

        return Response(data=cs.data)













