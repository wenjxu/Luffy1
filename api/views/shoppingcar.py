from rest_framework.response import Response
from rest_framework.views import APIView
from api import models
from api.utils.tool import BaseResponse
import traceback, json
from django.conf import settings
from django_redis import get_redis_connection
from api.utils.tool import PolicyPriceErro, ShoppingCartKeyErro


class ShoppingCart(APIView):
    conn = get_redis_connection('default')

    # 添加购物车
    def post(self, request, *args, **kwargs):
        '''
        :param request: courseid,policyid
        :param args:
        :param kwargs:
        :return:
        '''
        res = BaseResponse()

        try:
            # 1. 获取courseid课程id和policyid价格策略id,用户ID
            courseid = request.data.get("courseid")
            policyid = request.data.get("policyid")
            if not courseid or not policyid:
                raise ValueError("courseid或者policyid是空的")
            user_id = str(request.user.id)
            # print(courseid, policyid)

            # 2.获取courseid课程数据
            course_obj = models.Course.objects.get(id=courseid)

            # 3.获取价格策略的数据
            policy_objs = course_obj.price_policy.all()
            # print(policy_objs)

            pricepolicy = {}  # 价格策略
            for item in policy_objs:
                pricepolicy[str(item.id)] = {
                    "valid_period": item.get_valid_period_display(),
                    "valid_period_choices": item.valid_period,
                    "price": item.price,
                }
            # print(pricepolicy)

            # 4.获取配置信息购物车的key“shopping_car_2_2”
            shopping_cart_key = settings.SHOPPING_KEY % (user_id, courseid)
            # print(SHOPPING_KEY)

            # 5.判断policyid价格策略ID是否在该课程下存在
            if str(policyid) not in pricepolicy:
                raise PolicyPriceErro('该课程下没有该价格策略')

            # 判断redis中是否有重复的，期望不重复
            if not self.conn.exists(shopping_cart_key):
                # 6.将购物车的数据添加到redis中
                self.conn.hmset(shopping_cart_key, {
                    "name": course_obj.name,
                    "course_img": course_obj.course_img,
                    "pricepolicy": json.dumps(pricepolicy),
                    "default_policy": policyid
                })
                res.data = "添加成功"
            else:
                res.data = "重复提交"

        # 课程不存在异常
        except models.Course.DoesNotExist:
            res.code = 1002
            res.error = "提交的课程不存在"

        # 价格策略不存在异常
        except models.PricePolicy.DoesNotExist:
            res.code = 1003
            res.error = "提交的价格策略不存在"

        # 课程下没有该价格策略异常
        except PolicyPriceErro as e:
            res.code = 1005
            res.error = e.msg

        except Exception as e:
            res.code = 1001
            res.error = "添加购物车失败"
            # 未知错误，控制台打印错误
            traceback.print_exc()

        return Response(data=res.dict)

    # 查看购物车
    def get(self, request, *args, **kwargs):
        '''
        :param request: userID
        :param args:
        :param kwargs:
        :return: data
        '''
        res = BaseResponse()
        try:
            # 1.获取用户ID
            user_id = str(request.user.id)

            # 2.构建redis匹配模式,例如shopping_car_2_*
            shopping_cart_match = settings.SHOPPING_KEY % (user_id, '*')
            # print(self.conn.keys(SHOPPING_MATCH))

            # 3.# 构建每一条购物车的数据
            data = []
            for item in self.conn.scan_iter(shopping_cart_match, count=10):
                # print(self.conn.hgetall(item))
                dict = {}
                for key, value in self.conn.hgetall(item).items():
                    # 解码
                    key = key.decode('utf-8')
                    value = value.decode('utf-8')
                    dict[key] = value
                    # 反序列化
                    if key == "pricepolicy":
                        var = json.loads(value)
                        dict[key] = var  # 赋值反序列化后值
                data.append(dict)
            res.data = data

        except Exception:
            res.code = 1001
            res.error = "获取购物车数据失败"
            # 未知错误，控制台打印错误
            traceback.print_exc()

        return Response(data=res.dict)

    # 删除购物车
    def delete(self, request, *args, **kwargs):
        '''
        :param request: courseid
        :param args:
        :param kwargs:
        :return:
        '''
        res = BaseResponse()

        try:
            # 1.获取userID和courseid,courseid是多个值的列表
            user_id = str(request.user.id)
            # print(user_id)
            courseid = request.data.get("courseid")

            if not courseid:
                raise ValueError("courseid是空的")

            if not isinstance(courseid, list):
                raise ValueError("courseid类型错误")
            # print(type(courseid))

            # 2.循环courseID并且构造shopping_userID_courseID放入新列表中
            shopping_list = []
            for item in courseid:
                shopping_cart_key = settings.SHOPPING_KEY % (user_id, item)
                shopping_list.append(shopping_cart_key)
            # print(shopping_list)

            # 3.删除redis中记录，根据新列表这个删除
            ret = self.conn.delete(*shopping_list)
            if not ret:
                raise ShoppingCartKeyErro("购物车物品不存在")
            res.data = "删除成功"

        except ShoppingCartKeyErro as e:
            res.code = 1003
            res.error = e.msg

        except ValueError as e:
            res.code = 1002
            res.error = str(e)

        except Exception:
            res.code = 1001
            res.error = "删除失败"
            # 未知错误，控制台打印错误
            traceback.print_exc()

        return Response(res.dict)

    # 更新价格策略
    def patch(self, request, *args, **kwargs):
        '''
        :param request:courseid,policyid
        :param args:
        :param kwargs:
        :return:
        '''
        res = BaseResponse()
        try:
            # 1. 获取courseid课程id和policyid价格策略id,用户ID
            courseid = request.data.get("courseid")
            policyid = request.data.get("policyid")
            user_id = str(request.user.id)

            # print(courseid, policyid)
            if not courseid or not policyid:
                raise ValueError("courseid或者policyid是空的")

            # 2.拼接shopping_key，判断redis中是否有该物品
            shopping_cart_key = settings.SHOPPING_KEY % (user_id, courseid)
            print(shopping_cart_key)
            if self.conn.exists(shopping_cart_key):
                print(self.conn.hgetall(shopping_cart_key))

                # 3.判断课程下是否有policyid价格策略
                pricepolicy_dict = json.loads(self.conn.hget(shopping_cart_key, 'pricepolicy').decode("utf-8"))
                print(pricepolicy_dict)

                # 价格策略合法，修改default_policy的值
                if str(policyid) in pricepolicy_dict:
                    self.conn.hset(shopping_cart_key, "default_policy", policyid)
                    print("修改后的价格策略：", self.conn.hget(shopping_cart_key, "default_policy"))
                    res.data = "价格策略修改成功"
                else:
                    raise PolicyPriceErro("该课程下没有该价格策略")
            else:
                raise ShoppingCartKeyErro("购物车物品不存在")

        except ShoppingCartKeyErro as e:
            res.code = 1001
            res.error = e.msg

        except PolicyPriceErro as e:
            res.code = 1001
            res.error = e.msg

        except Exception:
            res.error = "更新失败"
            res.code = 1000
            # 未知错误，控制台打印错误
            traceback.print_exc()

        return Response(res.dict)





