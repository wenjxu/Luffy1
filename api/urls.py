from django.urls import path,re_path
from api.views import course,alipay
urlpatterns = [
    path('course/',course.CourseView.as_view({'get':'list'})),
    re_path('course/(?P<pk>\d+)/',course.CourseView.as_view({'get':'retrieve'})),
    path('index/',alipay.index)
]






