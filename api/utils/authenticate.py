from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from api import models
class AuthToken(BaseAuthentication):

    def authenticate(self, request):
        token = request.GET.get('token')
        token_obj = models.UserAuthToken.objects.filter(token=token).first()
        if token_obj:
            return token_obj.user.username, token_obj.token  # 返回两个值给request封装对象
        else:
            raise exceptions.AuthenticationFailed({'code': 1001, 'error': '认证失败'})






