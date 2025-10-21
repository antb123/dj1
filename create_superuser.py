#!/usr/bin/env python
"""Script to create a superuser for testing."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'document_manager.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser(
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created successfully!')
    print('Email: admin@example.com')
    print('Password: admin123')
else:
    print('Superuser already exists.')
