from api import models
from rest_framework import viewsets
from api.serializers.course import CourseSerializer,CourseDetailSerializer
from api.utils.wrapper import *
class CourseView(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    res = {'code': '1000', 'data': None}
    # 这个方法没有添加装饰器
    def retrieve(self, request, *args, **kwargs):
        try:
            pk =kwargs.get('pk')
            course_detail_obj = models.CourseDetail.objects.filter(pk=pk).first()
            cs = CourseDetailSerializer(course_detail_obj)
            self.res['data'] =cs.data
        except:
            traceback.print_exc()
            self.res['code'] ='1001'
        return Response(data=self.res)
        # 函数 = 装饰器(函数)

    @exception_wrapper
    def list(self, request, *args, **kwargs):
        course_objs = models.Course.objects.all()
        cs = CourseSerializer(course_objs,many=True)
        self.res['data'] = cs.data
        return Response(data=self.res)














