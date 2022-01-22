from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from user.models import AuthToken


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return None
        try:
            token = token.split(' ')
            if not len(token) == 2 or token[0] != 'Token':
                return None
            token = token[1]
            auth_token = AuthToken.objects.get(id=token)
            return (auth_token.user, auth_token)
        except Exception as e:
            return None
