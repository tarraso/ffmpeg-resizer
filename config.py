SECRET_KEY = "MYsECRET"

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

UPLOAD_FOLDER = '/tmp/uploads'