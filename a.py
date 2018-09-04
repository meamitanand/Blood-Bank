import os
BASE_DIR = os.path.dirname(os.path.dirname(os.getcwd()))
STATIC_ROOT = BASE_DIR

BASE_DIR = os.path.dirname(os.path.dirname(os.getcwd()))

STATICFILES_DIRS =os.path.join(BASE_DIR, '/Desktop/blooddonation-master/static/assets')
print (STATICFILES_DIRS)
