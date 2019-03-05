from rest_framework.throttling import SimpleRateThrottle

class VisitThrottle(SimpleRateThrottle):
    scope = 'luffy'
    def get_cache_key(self, request, view):
        return self.get_ident(request)













