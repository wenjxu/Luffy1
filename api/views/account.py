from rest_framework.views import APIView,Response
from api import models
import time,hashlib
def get_random_str(username):
    ctime =str(time.time())
    md5 = hashlib.md5()
    md5.update(bytes(str(username),encoding='utf-8'))
    md5.update(bytes(ctime,encoding='utf-8'))
    return md5.hexdigest()

class LoginView(APIView):
    authentication_classes = []
    def post(self,request):
        res = {"code":1000,'token':None}
        username = request.data.get('username')
        password = request.data.get('password')
        account_obj = models.Account.objects.filter(username=username,password=password).first()
        if account_obj:
            token = get_random_str(username)
            models.UserAuthToken.objects.update_or_create(user=account_obj,defaults={'token':token})
            res['token'] = token
        else:
            res['code'] =1001
        return Response(data=res)





