import os
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Luffy1.settings")
    import django
    django.setup()
    from django_redis import get_redis_connection

    conn = get_redis_connection("default")
    # var = conn.hgetall('user_token')
    # print(var)
    # conn.flushall()
    keys = conn.keys()
    print(keys)
    # print(conn.hgetall('shopping_car_2_2'))
    # print(conn.hgetall('shopping_car_2_1'))
    # conn.hset("test","key","value")
    # conn.expire("test",60)
    # ret = conn.delete("token_2")
    # print(ret)
    # print(ret)
    # ret = conn.hgetall("test")
    # print(ret)





