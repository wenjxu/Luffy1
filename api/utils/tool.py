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


class BaseResponse(object):
    def __init__(self):
        self.data = None
        self.code = 1000
        self.error = None
    @property
    def dict(self):
        return self.__dict__
