import os


import os
import firebase_admin
from firebase_admin import credentials

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework import authentication
from rest_framework import exceptions

from .exceptions import FirebaseError
from .exceptions import InvalidAuthToken
from .exceptions import NoAuthToken


cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "wejja-78a11",
  "private_key_id": "051c5673daa1c462147051a5e117c81ab65d1384",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC9vFmWuOIAsRZQ\nnDtqxpA/As6+obtTf1FlFQ5hxlU9An76OiCNXWjltfSDv8J+oObySs3kT/46OcNI\nqbFnrC8RciQEnXlsBvH1Mj3wSJz1D3Ag13oNva6luDcdeRhrGFCQS8pyeXNzukjL\ngkFmH0/ZdytCeRQmGmXOcugEi95N+e4NIV7vN4YbJEz1vyk8/87zXWJ2TJi105yX\nRwiNiHaPcjaMg9+KWhNBXiW5HhGb87M1hd3vxe6yWHCzNazvcSxHg3rkUuTS6zYs\nQ3wAT4yae9TozuaP49IDa5sMfbquRwglUZtvNAY07+e8VKvw/1orhVD8USsYv4Ci\n1C51bJtTAgMBAAECggEAALRopa43aCnlYdafGmRL1T+Qti46sy5vnycCWlfoPiys\nAVsWCzihyqihYweAJT4RCvMmHSQTTuJg8W/0j8OABeZvumRm9MtwhNI9mMh9z1VF\nmrNuDsEzmx8Afi3KMPoXoHKcQ4AysP/uAEFxNimBSdb5WAfcxnUh/2mYjoDtdXwI\np2xibJx5PjEcOjX2gMJl3ihKR64+KopCRNQ9GbaCMLGLD39p9GKmp7UkXWm+E29n\n4wB8lvOMeJvrNxfH2w0wB+daXZIMQsKfk/LjQrevrXxwT+soS1TdnkDHoG7cAZHi\n1zsD0lzCzIULh7UEhDuNdDxZepgXvaQ8Xj8jVdVI8QKBgQDjvyCW7WATsxr39q1v\npLD+1dJ0vbqp77BZW0EiMSVeE/ccE1ij1UMJ7xLa2BjBeVXw/DZ7TRIGn2o/vdl8\noAgDYVl4ibZV6GiHfT4HxqssyeB4xbMAvBelF1ooTStYIwl4rwnOagexiAXS9rTe\nTCRfAngTkzJL4Jpqbu+0vu7bPwKBgQDVRg7Z0o4vnsJ2WLQE5VIWtOMDdr98XmwY\n+RBJipjvY89cajfAOh5bCyDyBYwPDKKK+Mx0zMKgdh/5i9KtBrs0x1RWD2fP8vGr\nXjJSCVq/ePURIDTYsWYUVk+FsPgWx0QMoBesfwfTxQeckGVrkwGCrUufjD4jWWqO\nMqXQbBXe7QKBgQCjng0gwRrULEmEuXCyk4QhIKaY/jGborp0B85MbThmVTujrPZy\nhWUrPtmx5awrWyt1/Qx7GsyHe4HOl2snUKVRIGAx6+XV5CkspbqpxX32qHYe7hGC\nxp7KGXPJHl+0az+Dt2T5KU2rqohcnqckSVmb9F8l2Qs6Xfsx2c9WcBGT6wKBgHo6\nxJgiDEtOebTJ8aI8q2dIFDMQA36LvvgxBhyfyjaoxVb5qSoKJQuYvTD37OVTIHT1\nUng+Qe0kxf6HHB7+FJyTAMqx2ZVcbxT/z2ck5VWHRSyjgKYQRaiyLrE4U3b6jQ2P\nUwIRa7L64Pnh575Xai4yk3zFK3em72K/tDhXOdGhAoGBAMvqE0vcyz/fL3rwnIC5\n4FXeWTcnBqKUEcm+eY/VLK28ShybwTM+qVU835zzhdHKslCE64FVqARkKN8v9SIG\nfkvSqSxdI2/aOKWwMPNnmk4EZ6UAdwehQF0YLWDBR9tBg9a/EHRyLmE7R6TI4toI\nChBoWKfuN07H/ISFGXxYL0fw\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-3td65@wejja-78a11.iam.gserviceaccount.com",
  "client_id": "113732469645851820498",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3td65%40wejja-78a11.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

#default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        user, created = User.objects.get_or_create(username=uid)
        user.profile.last_activity = timezone.localtime()

        return (user, None)