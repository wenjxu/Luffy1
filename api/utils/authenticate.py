from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from api import models
from django_redis import get_redis_connection
import datetime
from django.conf import settings

EXPIRE_TIME = settings.TOKEN_EXPIRE_SECONDES  # token过期时间


class AuthToken(BaseAuthentication):
    conn = get_redis_connection("default")

    def authenticate(self, request):
        token = request.GET.get('token')
        token_obj = models.UserAuthToken.objects.filter(token=token).first()
        print(token_obj)
        if not token_obj:
            raise exceptions.AuthenticationFailed({'code': 1001, 'error': '认证失败'})
        # 如果token存在则在缓存中设置user_token
        return self.authenticate_credentials(token_obj)

    def authenticate_credentials(self, token_obj):
        '''
        :param token:
        :return: token,user
        '''

        # 判断缓存里面有没有过期
        if self.conn.hexists('user_token', token_obj.token):
            # 1.获取缓存中创建时间
            var = self.conn.hget('user_token', token_obj.token).decode("utf-8")
            print("redis中的存的token时间", var)
            print("现在的时间", datetime.datetime.now())

            # 2.转化成datatime格式
            get_time = datetime.datetime.strptime(var, "%Y-%m-%d %H:%M:%S.%f")
            print("token预算到期时间", get_time + datetime.timedelta(seconds=EXPIRE_TIME))

            # 3.判断缓存中时间加上比如：60秒是否小于当前时间，如果小于说明超过时间限制
            if get_time + datetime.timedelta(seconds=EXPIRE_TIME) < datetime.datetime.now():
                print("token时间已到过期")
                token_obj.is_delete = 1
                token_obj.save()
                raise exceptions.AuthenticationFailed('Token has expired then delete.')
            else:
                return token_obj.user.username, token_obj.token  # 返回两个值给request封装对象

                # 判断token对象是否存在并且is_delete=1
        if token_obj and token_obj.is_delete != 1:
            # 获取当前时间
            current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            # 设置缓存
            self.conn.hset('user_token', str(token_obj.token), current_time)
            print('redis设置token的数据：', self.conn.hgetall('user_token'))
        else:
            raise exceptions.AuthenticationFailed('Token has expired then delete.')