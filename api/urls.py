from django.urls import path,re_path
from api.views import course,alipay,account,article

urlpatterns = [

    path('course/',course.CourseView.as_view({'get':'list'})),
    path('course/<int:pk>/',course.CourseView.as_view({'get':'retrieve'})),
    path('index/',alipay.index),
    path('login/',account.LoginView.as_view()),
    path('article/',article.ArticleView.as_view({'get':'list'})),
    path('article/<int:pk>/',article.ArticleView.as_view({"get":"retrieve"})),
    path('comment/',article.CommentView.as_view({"get":"retrieve"})), # 传参：article_id

]






