import os
from .base import *

# Set the environment-specific settings
if os.getenv('DJANGO_ENV') == 'production':
    from .production import *
elif os.getenv('DJANGO_ENV') == 'development':
    from .development import *
else:
    from .local import *
