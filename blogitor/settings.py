from django.conf import settings

AUTH_USER_MODEL = settings.AUTH_USER_MODEL

POST_DEFAULT_LANGUAGE_CODE = getattr(
        settings, 'BLOGITOR_POST_DEFAULT_LANGUAGE_CODE',
        settings.LANGUAGE_CODE)

POST_ALLOW_COMMENTS_DEFAULT = getattr(
        settings, 'BLOGITOR_POST_ALLOW_COMMENTS_DEFAULT',
        True)
