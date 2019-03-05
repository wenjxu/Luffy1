from django.shortcuts import render, redirect
from api.utils.pay import AliPay
import time
from api import models

def index(request):
    if request.method =='GET':
        return render(request, 'index.html')

    PRI_KEY_PATH = "api/keys/app_private_2048.txt"
    PUB_KEY_PATH = "api/keys/alipay_public_2048.txt"
    obj = AliPay(
        appid='2016092800614112',
        app_notify_url="http://47.98.134.86:80/update_order/",  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成）
        return_url="http://47.98.134.86:80/pay_result/",  # 如果支付成功，重定向回到你的网站的地址。
        alipay_public_key_path=PUB_KEY_PATH,  # 支付宝公钥
        app_private_key_path=PRI_KEY_PATH,  # 应用私钥
        debug=True,  # 默认False,
    )
    alipay = obj

    # 对购买的数据进行加密
    money = float(request.POST.get('price'))
    out_trade_no = "x2" + str(time.time())
    # 1. 在数据库创建一条数据：状态（待支付）

    query_params = alipay.direct_pay(
        subject="充气式韩红",  # 商品简单描述
        out_trade_no=out_trade_no,  # 商户订单号
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
    )

    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

    return redirect(pay_url)

