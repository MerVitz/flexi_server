from datetime import datetime, timedelta

import jwt
from django.conf import settings


def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'user_type': user.user_type,
        'exp': datetime.utcnow() + timedelta(days=1),  # Token expiry
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
