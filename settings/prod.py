from .base import *


DEBUG = env.bool("DEBUG", default=False)

SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS')
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD')
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT')
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')

ADMINS = [
    ('Uwa Isibor', 'neutrolysis@gmail.com'),
]

DATABASES = {
    'default': {
    }
}
