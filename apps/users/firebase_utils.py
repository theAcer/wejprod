# firebase_utils.py

import pyrebase
from django.conf import settings

firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
auth = firebase.auth()