from rest_framework.throttling import SimpleRateThrottle


#Bu alttaki giris yapmamis kullanicinin register yapmasi durumunda tetiklenir
class RegisterThrottle(SimpleRateThrottle):
    scope = 'registerthrottle'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated or request.method == 'GET':
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }

#Bu alttaki giris yapmamis kullanicinin sayfayi yenilemesi durumunda tetiklenir
#ustteki gibi views/CreateUserView'e verebiliriz

# class RequestThrottle(AnonRateThrottle):
#     scope = 'registerthrottle'

#Bu alttaki hem giris yapmis hem de giris yapmamis kullanicinin sayfayi yenilemesi durumunda tetiklenir
#hem kullanicilarin hem de misafirlerin girebilecegi bir yerde throttle_classes olarak verebiliriz
#bi ustteki ile ayni isleve sahip

# class RequestThrottle(UserRateThrottle):
#     scope = 'registerthrottle'

#ScopedRateThrottle burada vermek yerine blog/settings icerisinde verip bir ustteki gibi