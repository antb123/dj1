# Django Document Management Application - Specification

## 1. Project Overview

A Django-based web application that allows users to manage and organize documents with a modern drag-and-drop interface. Users can upload various document formats, organize them into folders, and view analytics about their uploaded content.

## 2. Core Features

### 2.1 User Authentication

#### Registration
- Email-based registration system
- Required fields:
  - Email address (unique, validated)
  - Password (with confirmation)
  - First name (optional)
  - Last name (optional)
- Email verification workflow:
  - Send verification email upon registration
  - User must verify email before full access
- Password requirements:
  - Minimum 8 characters
  - Must contain letters and numbers
  - Password strength indicator

#### Login
- Email and password authentication
- "Remember me" option
- Password reset functionality via email
- Failed login attempt tracking (rate limiting)
- Session management with configurable timeout

#### User Profile
- View and edit profile information
- Change password functionality
- Account deletion option

### 2.2 Dashboard

The main interface after login, consisting of three primary sections:

#### Left Panel: Folder Navigation
- Tree-based folder structure
- Root folder (My Documents)
- Create new folders
- Rename folders
- Delete folders (with confirmation)
- Move folders via drag-and-drop
- Folder metadata:
  - Name
  - Creation date
  - Number of files
  - Total size
- Expandable/collapsible folder tree
- Search/filter folders

#### Center Panel: Document Upload & Management
- Drag-and-drop upload zone
- Click to browse and select files
- Multiple file upload support
- Supported file formats:
  - Text files (.txt)
  - Markdown files (.md)
  - PDF files (.pdf)
  - Word documents (.doc, .docx)
- Upload progress indicators
- File validation:
  - File type checking
  - File size limits (configurable, default: 10MB per file)
  - Virus scanning (optional integration)
- Document list view:
  - File name
  - File type icon
  - File size
  - Upload date
  - Actions (download, move, delete)
- Document actions:
  - Preview documents
  - Download documents
  - Move to different folder
  - Delete (with confirmation)
  - Rename
- Sorting options:
  - By name (A-Z, Z-A)
  - By date (newest/oldest)
  - By size (largest/smallest)
  - By type
- Bulk operations:
  - Select multiple files
  - Bulk move
  - Bulk delete
  - Bulk download (as ZIP)

#### Right Panel: Results & Analytics
- Real-time statistics:
  - Total number of files
  - Total storage used
  - Files by type breakdown
  - Recent uploads (last 10)
- Current folder statistics:
  - Number of files in selected folder
  - Total size of files in folder
  - File type distribution (chart/graph)
- Visual representations:
  - Pie chart for file type distribution
  - Bar chart for storage usage
  - Timeline of uploads
- Storage quota indicator:
  - Used vs. available storage
  - Visual progress bar
  - Warning when approaching limit

## 3. Technical Specifications

### 3.1 Backend (Django)

#### Models

**User Model**
- Extend Django's AbstractUser
- Fields:
  - email (unique, primary identifier)
  - first_name
  - last_name
  - is_email_verified
  - date_joined
  - last_login
  - storage_quota (default: 1GB)
  - storage_used

**Folder Model**
- Fields:
  - name
  - owner (ForeignKey to User)
  - parent (ForeignKey to self, nullable for root)
  - created_at
  - updated_at
  - path (for hierarchical queries)
- Methods:
  - get_full_path()
  - get_children()
  - get_file_count()
  - get_total_size()

**Document Model**
- Fields:
  - name
  - file (FileField)
  - file_type
  - file_size
  - owner (ForeignKey to User)
  - folder (ForeignKey to Folder)
  - uploaded_at
  - updated_at
  - checksum (for duplicate detection)
- Methods:
  - get_file_extension()
  - get_readable_size()
  - generate_preview()

#### Views/Endpoints

**Authentication**
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/verify-email/<token>/` - Email verification
- `/password-reset/` - Password reset request
- `/password-reset-confirm/<token>/` - Password reset confirmation

**Dashboard**
- `/dashboard/` - Main dashboard view

**API Endpoints (REST/JSON)**
- `/api/folders/` - List/create folders
- `/api/folders/<id>/` - Get/update/delete folder
- `/api/folders/<id>/move/` - Move folder
- `/api/documents/` - List/upload documents
- `/api/documents/<id>/` - Get/update/delete document
- `/api/documents/<id>/move/` - Move document
- `/api/documents/<id>/download/` - Download document
- `/api/documents/bulk-delete/` - Bulk delete documents
- `/api/statistics/` - Get user statistics
- `/api/statistics/folder/<id>/` - Get folder statistics

#### Django Apps Structure
```
document_manager/
├── accounts/           # User authentication and profile management
├── folders/           # Folder management
├── documents/         # Document upload and management
├── dashboard/         # Dashboard views and logic
└── api/              # REST API endpoints
```

### 3.2 Frontend

#### Technology Stack
- Django Templates (base structure)
- JavaScript (ES6+) for interactivity
- AJAX for asynchronous operations
- Recommended libraries:
  - Dropzone.js or similar for drag-and-drop uploads
  - Chart.js for analytics visualization
  - jQuery or vanilla JS for DOM manipulation
  - Bootstrap or Tailwind CSS for styling

#### Key JavaScript Components
- FileUploader: Handles drag-and-drop and file uploads
- FolderTree: Manages folder navigation and operations
- DocumentList: Displays and manages documents
- StatisticsPanel: Shows analytics and charts
- WebSocket or polling for real-time updates (optional)

### 3.3 Database
- PostgreSQL (recommended) or SQLite for development
- Indexes on:
  - User email
  - Document owner and folder
  - Folder owner and parent
- Full-text search capability for document names

### 3.4 Storage
- Local file storage for development
- Production options:
  - Amazon S3
  - Google Cloud Storage
  - Local file system with proper permissions
- Organized storage structure:
  ```
  media/
  └── documents/
      └── <user_id>/
          └── <folder_id>/
              └── <document_file>
  ```

### 3.5 Security

#### Authentication & Authorization
- Django session-based authentication
- CSRF protection enabled
- Rate limiting on login attempts
- Secure password hashing (Django default: PBKDF2)

#### File Security
- Validate file types on both client and server
- Scan for malicious content
- Prevent directory traversal attacks
- Serve files through Django views (not direct access)
- Generate secure, non-guessable filenames

#### Data Protection
- HTTPS only in production
- Secure cookie settings
- SQL injection protection (Django ORM)
- XSS protection
- Content Security Policy headers

### 3.6 Performance Considerations
- Lazy loading for folder trees
- Pagination for document lists
- Thumbnail generation for supported formats
- Database query optimization (select_related, prefetch_related)
- Caching for statistics
- Background tasks for heavy operations (Celery):
  - Email sending
  - File processing
  - Thumbnail generation

## 4. User Workflows

### 4.1 New User Registration
1. Navigate to registration page
2. Enter email and password
3. Submit registration form
4. Receive verification email
5. Click verification link
6. Redirect to login page
7. Login with credentials
8. Redirect to dashboard

### 4.2 Document Upload
1. Login to dashboard
2. Select target folder (or use root)
3. Drag files to upload zone OR click to browse
4. System validates files
5. Upload progress displayed
6. Files appear in document list
7. Statistics update in real-time

### 4.3 Folder Organization
1. Click "New Folder" button
2. Enter folder name
3. Folder appears in tree
4. Drag documents to folder
5. Drag folders to nest within others
6. View updated statistics

## 5. UI/UX Requirements

### 5.1 Responsive Design
- Desktop-first design
- Tablet compatibility
- Mobile responsive layout
- Minimum supported screen width: 320px

### 5.2 Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader friendly
- Proper ARIA labels
- Color contrast requirements
- Focus indicators

### 5.3 User Feedback
- Loading spinners for async operations
- Success/error messages (toast notifications)
- Confirmation dialogs for destructive actions
- Progress bars for uploads
- Disabled states for unavailable actions

## 6. Configuration & Settings

### 6.1 Django Settings
```python
# File upload settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ['.txt', '.md', '.pdf', '.doc', '.docx']

# Storage settings
DEFAULT_STORAGE_QUOTA = 1024 * 1024 * 1024  # 1GB

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_VERIFICATION_REQUIRED = True

# Security settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
LOGIN_ATTEMPTS_LIMIT = 5
```

### 6.2 Environment Variables
- SECRET_KEY
- DATABASE_URL
- EMAIL_HOST
- EMAIL_PORT
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
- STORAGE_BACKEND
- AWS_ACCESS_KEY_ID (if using S3)
- AWS_SECRET_ACCESS_KEY (if using S3)
- AWS_STORAGE_BUCKET_NAME (if using S3)

## 7. Testing Requirements

### 7.1 Unit Tests
- Model methods
- Form validation
- View logic
- API endpoints
- Utility functions

### 7.2 Integration Tests
- Complete user workflows
- File upload and download
- Folder operations
- Authentication flow

### 7.3 Security Tests
- Authentication bypass attempts
- Authorization checks
- File upload vulnerabilities
- SQL injection tests
- XSS tests

## 8. Deployment Considerations

### 8.1 Production Checklist
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configured
- [ ] Static files collected and served
- [ ] Media files storage configured
- [ ] Database migrations applied
- [ ] SSL/TLS certificate installed
- [ ] Environment variables set
- [ ] Backup strategy implemented
- [ ] Monitoring and logging configured
- [ ] Email service configured

### 8.2 Monitoring
- Error tracking (Sentry or similar)
- Application performance monitoring
- Storage usage monitoring
- User activity logging
- Failed login attempts tracking

## 9. Future Enhancements (V2)

### Potential Features
- Document sharing with other users
- Collaborative folder access
- Document versioning
- Full-text search within documents
- Document tags and metadata
- Comments on documents
- Activity feed/audit log
- API for third-party integrations
- Mobile apps (iOS/Android)
- Advanced file preview (in-browser PDF viewer, etc.)
- OCR for scanned documents
- Document conversion (e.g., DOC to PDF)
- Integration with cloud storage (Dropbox, Google Drive)
- Two-factor authentication
- Team/organization accounts
- Advanced analytics and reporting

---

**Document Version:** 1.0
**Last Updated:** 2025-10-11
**Status:** Draft