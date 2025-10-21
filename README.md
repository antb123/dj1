# Django Document Manager

A full-featured document management application built with Django that allows users to upload, organize, and manage their documents.

## Features

### User Authentication
- Email-based registration and login
- Email verification system
- Password reset functionality
- Secure session management

### Document Management
- **Drag-and-drop file upload** - Upload multiple files at once
- **Supported file types**: TXT, MD, PDF, DOC, DOCX
- **File size limit**: 10MB per file
- **Storage quota**: 1GB per user
- Download documents
- Delete documents
- File preview support

### Folder Organization
- Create folders to organize documents
- Hierarchical folder structure (nested folders)
- Move documents between folders
- Rename and delete folders
- Track files per folder

### Dashboard Features
- **Three-panel layout**:
  - **Left panel**: Folder navigation tree
  - **Center panel**: Document list with upload zone
  - **Right panel**: Statistics and analytics

### Statistics & Analytics
- Real-time storage usage indicator
- Total files and folders count
- File type distribution (pie chart)
- Recent uploads timeline
- Storage quota visualization

## Installation

### Prerequisites
- Python 3.8+
- pip
- Django 4.2+

### Setup Instructions

1. **Navigate to the project directory**:
   ```bash
   cd /home/antb2/dev/rsync/dj1
   ```

2. **Install dependencies** (if using virtualenv):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser** (optional, for admin access):
   ```bash
   python create_superuser.py
   ```
   Or manually:
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Main app: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Default Credentials

A test superuser has been created:
- **Email**: admin@example.com
- **Password**: admin123

## Usage

### Registration
1. Navigate to http://localhost:8000/
2. Click "Register here"
3. Fill in your email and password
4. Check console output for verification email (in development mode)
5. Click the verification link
6. Login with your credentials

### Upload Documents
1. Login to the dashboard
2. Drag and drop files into the upload zone, or click to browse
3. Files will be uploaded to the currently selected folder
4. View uploaded files in the center panel

### Organize with Folders
1. Click the "+" button in the folder panel
2. Enter a folder name
3. Click on folders to view their contents
4. Drag documents to move them between folders

### View Statistics
- Check the right panel for:
  - Storage usage and available space
  - Total files and folders count
  - File type distribution chart
  - Recent upload activity

## Project Structure

```
document_manager/
├── accounts/           # User authentication and profile management
│   ├── models.py      # Custom User model
│   ├── views.py       # Login, registration, email verification
│   ├── forms.py       # Authentication forms
│   └── urls.py        # Auth-related URLs
├── folders/           # Folder management
│   ├── models.py      # Folder model
│   └── admin.py       # Admin configuration
├── documents/         # Document upload and management
│   ├── models.py      # Document model
│   └── admin.py       # Admin configuration
├── dashboard/         # Main dashboard
│   ├── views.py       # Dashboard view with statistics
│   └── urls.py        # Dashboard URLs
├── api/              # REST API endpoints
│   ├── views.py       # API views for folders and documents
│   └── urls.py        # API URLs
├── templates/        # HTML templates
│   ├── base.html     # Base template
│   ├── accounts/     # Auth templates
│   └── dashboard/    # Dashboard template
├── static/           # Static files (CSS, JS)
├── media/            # Uploaded files
└── manage.py         # Django management script
```

## API Endpoints

### Folders
- `GET /api/folders/` - List all folders
- `POST /api/folders/` - Create a new folder
- `GET /api/folders/<id>/` - Get folder details
- `PUT /api/folders/<id>/` - Update folder
- `DELETE /api/folders/<id>/` - Delete folder

### Documents
- `GET /api/documents/` - List all documents
- `POST /api/documents/` - Upload documents
- `GET /api/documents/<id>/` - Get document details
- `DELETE /api/documents/<id>/` - Delete document
- `GET /api/documents/<id>/download/` - Download document

## Configuration

### Settings (document_manager/settings.py)

```python
# File upload settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ['.txt', '.md', '.pdf', '.doc', '.docx']

# Storage settings
DEFAULT_STORAGE_QUOTA = 1024 * 1024 * 1024  # 1GB

# Email settings (console backend for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Security settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
```

### Email Configuration
For production, update email settings in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

## Security Features

- CSRF protection enabled
- Password hashing with PBKDF2
- Email verification required
- Session-based authentication
- File type validation
- File size limits
- Storage quota enforcement
- Secure file serving (files served through Django views)

## Technologies Used

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5.3, jQuery, Chart.js
- **Database**: SQLite (development) - can be configured for PostgreSQL/MySQL
- **File Storage**: Local filesystem (can be configured for S3/Cloud Storage)

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Troubleshooting

### Issue: Email verification not working
**Solution**: In development mode, emails are printed to the console. Check the terminal output for verification links.

### Issue: Files not uploading
**Solution**:
1. Check file size (max 10MB)
2. Check file type is allowed
3. Check storage quota not exceeded
4. Ensure `media/` directory exists and has proper permissions

### Issue: Static files not loading
**Solution**:
1. Run `python manage.py collectstatic`
2. Check `STATIC_URL` and `STATICFILES_DIRS` in settings
3. Ensure DEBUG=True for development

## Future Enhancements

- Document sharing between users
- Document versioning
- Full-text search
- Advanced file preview
- Bulk operations
- Tags and metadata
- Activity logs
- Mobile app

## License

This project is built for demonstration purposes.

## Support

For issues and questions, please check:
1. The SPEC.md file for detailed specifications
2. Django documentation: https://docs.djangoproject.com/
3. Bootstrap documentation: https://getbootstrap.com/docs/

---

**Built with Django and Bootstrap**
