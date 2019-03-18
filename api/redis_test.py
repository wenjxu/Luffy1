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





