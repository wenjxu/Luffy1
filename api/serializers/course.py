from api import models
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields ='__all__'

class CourseDetailSerializer(serializers.ModelSerializer):
    course_title = serializers.SerializerMethodField()
    recommend_courses = serializers.SerializerMethodField()
    teachers = serializers.SerializerMethodField()

    def get_course_title(self, obj):
        return obj.course.name

    def get_recommend_courses(self, obj):
        course_objs = obj.recommend_courses.all()
        return [item.name for item in course_objs]

    def get_teachers(self,obj):
        course_objs = obj.teachers.all()
        return [item.name for item in course_objs]

    class Meta:
        model =models.CourseDetail
        fields = '__all__'















