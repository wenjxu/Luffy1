from api import models
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()  # 课程子类
    price_policy = serializers.SerializerMethodField()  # 价格策略
    # category = serializers.SerializerMethodField()
    def get_sub_category(self,obj):
        sub_category_obj = obj.sub_category
        category_obj = obj.sub_category.category
        return {
            'name':sub_category_obj.name,
            'category':{'name':category_obj.name},
        }
    def get_price_policy(self,obj):
        price_policy_objs = obj.price_policy.all()
        print(price_policy_objs)
        return [{

            'id':item.id,
            'valid_period':item.get_valid_period_display(),
            'price':item.price,

        } for item in price_policy_objs]

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















