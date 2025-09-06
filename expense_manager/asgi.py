# expense_manager/asgi.py

import os
from django.core.asgi import get_asgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_manager.settings')

# Create ASGI application
application = get_asgi_application()
