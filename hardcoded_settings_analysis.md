# Hardcoded Settings Analysis - Django Document Manager

## Overview
This document provides a detailed analysis of all hardcoded settings found in the Django Document Manager codebase that should be moved to environment variables for better security, flexibility, and maintainability.

## 1. Security Settings (Critical)

### 1.1 Secret Key
**Location**: [`document_manager/settings.py:24`](document_manager/settings.py:24)
```python
SECRET_KEY = 'django-insecure-z&x&9er45hkfe3nb4tgf#_iga0(z1xm0_-met5&+19q)+mtz-b'
```
**Risk**: Exposed in source control, same key across all environments
**Impact**: Session hijacking, CSRF token forgery, security breach

### 1.2 Debug Mode
**Location**: [`document_manager/settings.py:27`](document_manager/settings.py:27)
```python
DEBUG = True
```
**Risk**: Always enabled, exposes sensitive information in production
**Impact**: Information disclosure, security vulnerabilities exposure

### 1.3 Allowed Hosts
**Location**: [`document_manager/settings.py:29`](document_manager/settings.py:29)
```python
ALLOWED_HOSTS = []
```
**Risk**: Empty list allows any host in debug mode
**Impact**: Host header injection attacks

## 2. File Upload Settings

### 2.1 Maximum Upload Size
**Location**: [`document_manager/settings.py:151`](document_manager/settings.py:151)
```python
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
```
**Issue**: Hardcoded 10MB limit, not configurable per environment
**Impact**: Cannot adjust limits for different deployment scenarios

### 2.2 Allowed File Types
**Location**: [`document_manager/settings.py:152`](document_manager/settings.py:152)
```python
ALLOWED_FILE_TYPES = ['.txt', '.md', '.pdf', '.doc', '.docx']
```
**Issue**: File type restrictions embedded in code
**Impact**: Requires code deployment to change allowed file types

### 2.3 Storage Quota
**Location**: [`document_manager/settings.py:155`](document_manager/settings.py:155)
```python
DEFAULT_STORAGE_QUOTA = 1024 * 1024 * 1024  # 1GB
```
**Issue**: Fixed 1GB quota for all users
**Impact**: Cannot offer different tiers or adjust based on resources

## 3. Session & Security Settings

### 3.1 Session Cookie Age
**Location**: [`document_manager/settings.py:158`](document_manager/settings.py:158)
```python
SESSION_COOKIE_AGE = 1209600  # 2 weeks
```
**Issue**: Fixed 2-week session timeout
**Impact**: Cannot adjust based on security requirements

### 3.2 Password Reset Timeout
**Location**: [`document_manager/settings.py:159`](document_manager/settings.py:159)
```python
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
```
**Issue**: Fixed 1-hour password reset window
**Impact**: Cannot adjust based on security policies

## 4. Email Settings

### 4.1 Email Backend
**Location**: [`document_manager/settings.py:147`](document_manager/settings.py:147)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
**Issue**: Hardcoded console backend for all environments
**Impact**: Cannot send real emails in production without code changes

### 4.2 Default From Email
**Location**: [`document_manager/settings.py:148`](document_manager/settings.py:148)
```python
DEFAULT_FROM_EMAIL = 'noreply@documentmanager.com'
```
**Issue**: Fixed sender email address
**Impact**: Cannot customize for different domains or environments

## 5. Database Settings

### 5.1 Database Configuration
**Location**: [`document_manager/settings.py:83-88`](document_manager/settings.py:83)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
**Issue**: Hardcoded SQLite for all environments
**Impact**: Cannot use PostgreSQL/MySQL in production without code changes

## 6. Model Default Values

### 6.1 User Storage Quota
**Location**: [`accounts/models.py:40`](accounts/models.py:40)
```python
storage_quota = models.BigIntegerField(default=1024*1024*1024)  # 1GB default
```
**Issue**: Duplicate hardcoded 1GB quota
**Impact**: Inconsistent if settings change, requires database migration

### 6.2 File Type Mapping
**Location**: [`documents/models.py:64-71`](documents/models.py:64)
```python
ext_to_type = {
    '.txt': 'txt',
    '.md': 'md',
    '.pdf': 'pdf',
    '.doc': 'doc',
    '.docx': 'docx',
}
```
**Issue**: File type mapping hardcoded in model
**Impact**: Cannot extend file types without code changes

## 7. Frontend Configuration

### 7.1 CDN URLs
**Location**: [`templates/base.html:7-8`](templates/base.html:7)
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
```
**Issue**: External CDN URLs hardcoded
**Impact**: Dependency on external services, no fallback option

### 7.2 Chart.js CDN
**Location**: [`templates/dashboard/index.html:261`](templates/dashboard/index.html:261)
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```
**Issue**: External dependency hardcoded
**Impact**: No version pinning, potential breaking changes

## 8. API Configuration

### 8.1 File Upload Accept Attribute
**Location**: [`templates/dashboard/index.html:129`](templates/dashboard/index.html:129)
```html
<input type="file" id="fileInput" multiple hidden accept=".txt,.md,.pdf,.doc,.docx">
```
**Issue**: File types duplicated in frontend
**Impact**: Must update in multiple places when changing

## 9. Management Commands

### 9.1 Default Superuser Credentials
**Location**: [`create_superuser.py:14-16`](create_superuser.py:14)
```python
email='admin@example.com',
password='admin123',
```
**Risk**: Hardcoded admin credentials
**Impact**: Security vulnerability if script used in production

## 10. Recommended Environment Variables

### 10.1 .env File Structure
```bash
# Security
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=document_manager
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# File Upload
MAX_UPLOAD_SIZE_MB=10
ALLOWED_FILE_TYPES=.txt,.md,.pdf,.doc,.docx
DEFAULT_STORAGE_QUOTA_GB=1

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Security Sessions
SESSION_COOKIE_AGE_SECONDS=1209600
PASSWORD_RESET_TIMEOUT_SECONDS=3600

# External Services
USE_CDN=True
BOOTSTRAP_VERSION=5.3.0
BOOTSTRAP_ICONS_VERSION=1.10.0
CHART_JS_VERSION=3.9.1
```

### 10.2 Updated Settings Configuration
```python
# document_manager/settings.py
import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

# File Upload Settings
MAX_UPLOAD_SIZE = config('MAX_UPLOAD_SIZE_MB', default=10, cast=int) * 1024 * 1024
ALLOWED_FILE_TYPES = config(
    'ALLOWED_FILE_TYPES',
    default='.txt,.md,.pdf,.doc,.docx',
    cast=Csv()
)
DEFAULT_STORAGE_QUOTA = config(
    'DEFAULT_STORAGE_QUOTA_GB',
    default=1,
    cast=int
) * 1024 * 1024 * 1024

# Email Settings
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@documentmanager.com')

# Security Settings
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE_SECONDS', default=1209600, cast=int)
PASSWORD_RESET_TIMEOUT = config('PASSWORD_RESET_TIMEOUT_SECONDS', default=3600, cast=int)

# External Services
USE_CDN = config('USE_CDN', default=True, cast=bool)
BOOTSTRAP_VERSION = config('BOOTSTRAP_VERSION', default='5.3.0')
BOOTSTRAP_ICONS_VERSION = config('BOOTSTRAP_ICONS_VERSION', default='1.10.0')
CHART_JS_VERSION = config('CHART_JS_VERSION', default='3.9.1')
```

### 10.3 Template Context for Dynamic CDN URLs
```python
# document_manager/context_processors.py
def cdn_urls(request):
    """Provide CDN URLs to templates."""
    return {
        'use_cdn': settings.USE_CDN,
        'bootstrap_version': settings.BOOTSTRAP_VERSION,
        'bootstrap_icons_version': settings.BOOTSTRAP_ICONS_VERSION,
        'chart_js_version': settings.CHART_JS_VERSION,
    }

# Add to settings.py TEMPLATES context_processors
TEMPLATES = [
    {
        # ... other settings
        'OPTIONS': {
            'context_processors': [
                # ... existing processors
                'document_manager.context_processors.cdn_urls',
            ],
        },
    },
]
```

### 10.4 Updated Template with Conditional CDN
```html
<!-- templates/base.html -->
{% if use_cdn %}
<link href="https://cdn.jsdelivr.net/npm/bootstrap@{{ bootstrap_version }}/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@{{ bootstrap_icons_version }}/font/bootstrap-icons.css">
{% else %}
<link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
<link rel="stylesheet" href="{% static 'css/bootstrap-icons.css' %}">
{% endif %}
```

## 11. Priority Implementation Order

### High Priority (Security Critical)
1. **SECRET_KEY** - Move to environment variable immediately
2. **DEBUG=False** - Never True in production
3. **ALLOWED_HOSTS** - Configure for production domains
4. **Database credentials** - Move to environment variables

### Medium Priority (Functionality)
1. **Email settings** - Configure for production email sending
2. **File upload limits** - Make configurable
3. **Storage quotas** - Make environment-specific
4. **Session timeouts** - Configure based on security policies

### Low Priority (Optimization)
1. **CDN URLs** - Make configurable with fallbacks
2. **File type mappings** - Move to configuration
3. **Frontend versions** - Pin and make configurable

## 12. Security Considerations

### 12.1 Sensitive Data Exposure
- Never commit `.env` files to version control
- Add `.env` to `.gitignore`
- Use different secrets for development, staging, and production
- Rotate secrets regularly

### 12.2 Environment-Specific Configuration
- Use separate `.env.development`, `.env.staging`, `.env.production`
- Validate required environment variables on startup
- Provide sensible defaults for development

### 12.3 Configuration Validation
```python
# document_manager/validators.py
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
import os

def validate_settings():
    """Validate critical settings on startup."""
    required_settings = [
        'SECRET_KEY',
        'ALLOWED_HOSTS',
    ]
    
    for setting in required_settings:
        if not getattr(settings, setting, None):
            raise ImproperlyConfigured(f"Required setting {setting} is not configured")
    
    if settings.DEBUG and not settings.ALLOWED_HOSTS:
        raise ImproperlyConfigured("ALLOWED_HOSTS cannot be empty in production")

# Call in document_manager/wsgi.py and asgi.py
```

## Conclusion

The Django Document Manager has numerous hardcoded settings that pose security risks and limit flexibility. Moving these to environment variables is essential for:
- **Security**: Preventing exposure of sensitive credentials
- **Flexibility**: Supporting different deployment environments
- **Maintainability**: Changing configuration without code deployments
- **Scalability**: Adjusting settings based on resources and requirements

The implementation should prioritize security-critical settings first, followed by functional requirements, and finally optimization opportunities.