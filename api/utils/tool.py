import traceback
from rest_framework.views import Response

def exception_wrapper(func):
    res = {'code': '1000', 'data': None}
    def wrapper(request, *args, **kwargs):
        try:
            ret = func(request, *args, **kwargs)
            return ret
        except Exception:
            res['code'] = '1001'
            traceback.print_exc()
            return Response(data=res)
    return wrapper

# 构造Response
class BaseResponse(object):
    def __init__(self):
        self.data = None
        self.code = 1000
        self.error = None
    @property
    def dict(self):
        return self.__dict__

# 自定义异常类
class PolicyPriceErro(Exception): # 价格策略不存在错误
    def __init__(self,msg):
        self.msg = msg
class ShoppingCartKeyErro(Exception): # 购物车物品不存在错误
    def __init__(self,msg):
        self.msg = msg



