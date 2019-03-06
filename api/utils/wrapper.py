import traceback
from rest_framework.views import Response
def exception_wrapper(func):
    res = {'code': '1000', 'data': None}
    def wrapper(request, *args, **kwargs):
        try:
            ret = func(request, *args, **kwargs)
            return ret
        except:
            res['code'] = '1001'
            traceback.print_exc()
            return Response(data=res)
    return wrapper

