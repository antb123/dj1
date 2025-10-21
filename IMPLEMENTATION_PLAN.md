# Django Micro-Lending Platform - Implementation Plan & Specification

## Executive Summary

This document outlines the complete transformation of the Django Document Management System into a **mobile-first micro-lending platform** with WhatsApp OTP authentication, KYC verification, scoring system, and borrowing functionality. The system is optimized for African markets with low-bandwidth phones and minimal JavaScript.

---

## Phase 1: Authentication System (COMPLETED)

### 1.1 WhatsApp OTP Authentication
- **Status**: ✅ COMPLETED
- **Implementation**:
  - Created `whatsapp_auth` app with models: `WhatsAppUser`, `OTP`
  - Twilio WhatsApp API integration (SDK added to requirements.txt)
  - OTP generation (6-digit codes, 5-minute expiry)
  - Views: `RequestOTPView`, `VerifyOTPView`, `LogoutView`
  - URLs: `/auth/request-otp/`, `/auth/verify-otp/`, `/auth/logout/`

### 1.2 User Model Changes
- **Status**: ✅ COMPLETED
- **Changes**:
  - Replaced `email` with `phone_number` (unique identifier)
  - Removed `is_email_verified` field
  - Added new fields:
    - `kyc_level` (0-2)
    - `score` (integer, default 0)
    - `aid_recipient` (boolean, default True)
  - Updated `UserManager` for phone-based authentication
  - Updated Django Admin interface

### 1.3 Database
- **Status**: ✅ COMPLETED
- Migrations created and applied
- All new apps registered in `INSTALLED_APPS`

---

## Phase 2: KYC System (COMPLETED)

### 2.1 KYC Models
- **Status**: ✅ COMPLETED
- **Models Created**:

#### KYCProfile
```python
- user: OneToOneField(User)
- full_name: CharField
- date_of_birth: DateField
- city: CharField
- mobile_money_number: CharField
- id_type: CharField
- id_number: CharField
- has_business: BooleanField
- is_only_owner: BooleanField
- business_description: TextField
- loan_purpose: TextField
- all_questions_answered: BooleanField
- level_1_completed_at: DateTimeField
- business_registration_doc: FileField (Level 2)
- electricity_bill_doc: FileField (Level 2)
- level_2_completed_at: DateTimeField
- unique_identifier property: phone + DOB + ID
```

#### QuestionnaireResponse
```python
- kyc_profile: ForeignKey(KYCProfile)
- question_index: IntegerField (0-9)
- question_text: TextField
- answer: TextField
- answered_at: DateTimeField
```

#### KYCDocument
```python
- kyc_profile: ForeignKey(KYCProfile)
- document_type: CharField (business_registration, electricity_bill, etc.)
- document_file: FileField
- uploaded_at: DateTimeField
- verified: BooleanField
- verified_by: ForeignKey(User, admin)
- verified_at: DateTimeField
```

### 2.2 KYC Questions (from settings.py)
```python
1. "Say your full name as on your ID. (You can also type.)"
2. "Date of birth. Use keypad: DDMMYYYY."
3. "City or village where you live. (You can say nearest market or landmark.)"
4. "Mobile money number. Use keypad."
5. "ID type. Say: national ID, voter card, passport, or other."
6. "ID number. Use keypad."
7. "You have a business ? Press 1 Yes, 2 No."
8. "Are you the only owner? Press 1 Yes, 2 No."
9. "What do you do or sell? One sentence."
10. "Loan purpose in one sentence."
```

### 2.3 KYC Workflow
- User completes all 10 questions → KYC Level 1 assigned
- Unique key: `phone_number + DOB + ID_number`
- User uploads business registration + electricity bill → KYC Level 2 assigned
- Admin verifies documents before level 2 approval

---

## Phase 3: Scoring System (COMPLETED)

### 3.1 Scoring Models
- **Status**: ✅ COMPLETED

#### ScoreLog
```python
- user: ForeignKey(User)
- reason: CharField (referral, phone_bill, admin_adjustment, other)
- points_added: IntegerField
- previous_score: IntegerField
- new_score: IntegerField
- notes: TextField
- created_at: DateTimeField (auto)
```

#### PhoneBillUpload
```python
- user: ForeignKey(User)
- phone_bill_file: FileField
- uploaded_at: DateTimeField
- verified: BooleanField
- verified_by: ForeignKey(User, admin)
- verified_at: DateTimeField
- score_awarded: BooleanField
```

#### Referral
```python
- referrer: ForeignKey(User)
- referred_user: ForeignKey(User, nullable)
- referral_code: CharField (unique, 8 chars)
- referred_phone: CharField
- score_awarded: BooleanField
- created_at: DateTimeField
```

#### ScoreRule
```python
- rule_name: CharField (unique)
- rule_type: CharField (referral, phone_bill, kyc_level_1, kyc_level_2, other)
- points_value: IntegerField
- is_active: BooleanField
- created_at, updated_at: DateTimeField
```

### 3.2 Scoring Logic
- **Base Referral Points**: 50 (configurable via ScoreRule)
- **Phone Bill Upload Points**: 25 (configurable via ScoreRule)
- **Triggers**:
  - User refers someone → Add referral points
  - User uploads phone bill (admin approved) → Add phone bill points
  - Admin adjustment → Add/subtract points
- **Score Impact**: Higher score + higher KYC level = higher borrow limit

---

## Phase 4: Borrowing System (COMPLETED)

### 4.1 Borrowing Models
- **Status**: ✅ COMPLETED

#### BorrowLimit
```python
- user: OneToOneField(User)
- max_borrow_amount: DecimalField (default 20)
- available_borrow: DecimalField
- is_locked: BooleanField (default True, unlocked when KYC L1)
- created_at, updated_at: DateTimeField
```

#### BorrowTransaction
```python
- user: ForeignKey(User)
- amount_before: DecimalField (available before)
- amount_requested: DecimalField
- borrow_fee: DecimalField (calculated)
- amount_debit: DecimalField (requested + fee)
- amount_after: DecimalField (available after)
- status: CharField (pending, approved, rejected, completed, repaid)
- processed: BooleanField
- created_at, processed_at, repaid_at: DateTimeField
```

#### BorrowRepayment
```python
- transaction: ForeignKey(BorrowTransaction)
- amount_paid: DecimalField
- repaid_at: DateTimeField
- notes: TextField
```

### 4.2 Borrowing Workflow
1. User selects borrow amount
2. System checks: KYC Level 1 unlocked? Available balance? Score adequate?
3. Display fee warning (BORROW_FEE_PERCENT = 5% from settings)
4. Create BorrowTransaction with `status=pending`
5. Admin approval → `status=approved, processed=True`
6. Update `BorrowLimit.available_borrow`
7. Display transaction history

---

## Phase 5: Frontend Templates (COMPLETED)

### 5.1 Base Template
- **File**: `templates/base.html`
- **Size**: < 20KB (inline CSS, no Bootstrap)
- **Features**:
  - Mobile-optimized (max-width: 500px)
  - Zero JavaScript dependencies
  - Minimal CSS classes
  - Fast loading for low-bandwidth phones

### 5.2 Authentication Templates

#### `templates/whatsapp_auth/request_otp.html`
- Phone number input with country code
- Send OTP button
- Minimal styling
- AJAX support (XMLHttpRequest)

#### `templates/whatsapp_auth/verify_otp.html`
- 6-digit OTP input
- Verify button
- Link to re-enter phone
- Error handling
- AJAX support

### 5.3 Dashboard Template
- **File**: `templates/dashboard/index.html`
- **Sections**:
  1. Header with welcome message
  2. KYC Status card (Locked/Level 1/Level 2 badges)
  3. Score display
  4. Borrowing status (locked/unlocked with amount)
  5. Recent transactions (if any)
  6. Referral invite section
  7. Phone bill upload section
  8. Logout link
  9. Bottom navigation (Home, KYC, Refer, Account)

---

## Phase 6: Configuration (COMPLETED)

### 6.1 Settings.py Updates
```python
# WhatsApp/Twilio
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER', default='whatsapp:+1234567890')

# OTP
OTP_VALID_DURATION = 300  # 5 minutes
OTP_MAX_ATTEMPTS = 3

# KYC
KYC_LEVEL_1_THRESHOLD = 10  # All questions answered
KYC_LEVEL_2_REQUIRES = ['business_registration', 'electricity_bill']

# Scoring
BASE_REFERRAL_POINTS = 50
PHONE_BILL_UPLOAD_POINTS = 25

# Borrowing
MAX_INITIAL_BORROW = 20
BORROW_FEE_PERCENT = 5
```

### 6.2 Environment Variables Required
```
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_WHATSAPP_NUMBER
SECRET_KEY
DEBUG
ALLOWED_HOSTS
DATABASE_URL (optional)
```

---

## Phase 7: Apps Structure

### Current Project Structure
```
document_manager/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── document_manager/
│   ├── settings.py (UPDATED)
│   ├── urls.py (UPDATED)
│   └── wsgi.py
├── accounts/
│   ├── models.py (UPDATED - phone-based)
│   ├── views.py
│   ├── admin.py (UPDATED)
│   └── migrations/
├── whatsapp_auth/ (NEW)
│   ├── models.py (OTP, WhatsAppUser)
│   ├── views.py (RequestOTP, VerifyOTP, Logout)
│   ├── urls.py
│   └── migrations/
├── kyc/ (NEW)
│   ├── models.py (KYCProfile, QuestionnaireResponse, KYCDocument)
│   ├── admin.py
│   └── migrations/
├── scoring/ (NEW)
│   ├── models.py (ScoreLog, PhoneBillUpload, Referral, ScoreRule)
│   ├── admin.py
│   └── migrations/
├── borrowing/ (NEW)
│   ├── models.py (BorrowLimit, BorrowTransaction, BorrowRepayment)
│   ├── admin.py
│   └── migrations/
├── dashboard/
│   ├── views.py (UPDATED - lending dashboard)
│   ├── urls.py
│   └── migrations/
├── templates/
│   ├── base.html (UPDATED - lightweight)
│   ├── whatsapp_auth/
│   │   ├── request_otp.html (NEW)
│   │   └── verify_otp.html (NEW)
│   └── dashboard/
│       └── index.html (UPDATED - lending dashboard)
└── static/
    └── (minimal - no static files needed)
```

### Apps Removed (For Cleanup)
- `documents/` (document upload/management)
- `folders/` (folder organization)
- `api/` (old REST API)

---

## Phase 8: Remaining Implementation Tasks

### TODO: To Be Implemented
1. **KYC Views & Forms**
   - Questionnaire display form
   - Answer submission & validation
   - Document upload for Level 2
   - KYC admin approval workflow

2. **Scoring Views**
   - Referral link generation
   - Phone bill upload interface
   - Score history display
   - Referral tracking

3. **Borrowing Views**
   - Borrow request form
   - Amount selection with fee display
   - Transaction approval workflow
   - Repayment tracking

4. **API Endpoints**
   - `/api/kyc/status/` - GET KYC status
   - `/api/kyc/questionnaire/submit/` - POST answers
   - `/api/kyc/documents/upload/` - POST documents
   - `/api/score/` - GET score info
   - `/api/score/invite/` - GET referral link
   - `/api/borrowing/check-limit/` - GET available amount
   - `/api/borrowing/borrow/` - POST borrow request
   - `/api/borrowing/transactions/` - GET transaction history

5. **Admin Interface**
   - KYC approval dashboard
   - Score rule management
   - Document verification
   - Transaction monitoring
   - User management

6. **Security & Optimization**
   - Input validation on all forms
   - File upload security
   - Rate limiting
   - Caching for statistics
   - Background tasks (Celery) for email/processing

7. **Testing**
   - Unit tests for models
   - Integration tests for workflows
   - Security tests (auth bypass, injection, etc.)

8. **Documentation**
   - API documentation
   - Admin user guide
   - Deployment checklist

---

## Deployment Checklist

- [ ] Set all environment variables
- [ ] Configure email backend (SMTP)
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Run migrations
- [ ] Create superuser
- [ ] Collect static files
- [ ] Configure file storage (local/S3)
- [ ] Set up logging
- [ ] Configure SSL/TLS
- [ ] Set up database backups
- [ ] Test Twilio WhatsApp integration

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Django 5.0.1 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Authentication | WhatsApp OTP via Twilio |
| Frontend | Plain HTML/CSS (< 20KB) |
| JavaScript | Minimal (AJAX only) |
| File Storage | Local (dev) / S3 (prod) |
| Background Tasks | Celery (optional) |

---

## Key Decisions

1. ✅ **WhatsApp OTP**: Using Twilio API for reliable SMS delivery
2. ✅ **Phone-Based Auth**: No email required, perfect for African markets
3. ✅ **Lightweight Frontend**: Plain CSS/HTML to support low-bandwidth phones
4. ✅ **Minimal JavaScript**: Only AJAX for form submission, no frameworks
5. ✅ **Text Input Only**: No voice processing for MVP (can add later)
6. ✅ **Local File Storage**: Simpler for MVP, can migrate to S3 later
7. ✅ **Admin-First Verification**: KYC/documents verified by admins before approval
8. ✅ **Configurable Rules**: All fees/points configurable via Django admin

---

## File Size Optimization

| Component | Size |
|-----------|------|
| base.html | ~4 KB |
| request_otp.html | ~1 KB |
| verify_otp.html | ~1 KB |
| dashboard/index.html | ~3 KB |
| Total CSS (inline) | ~8 KB |
| **Total Page Load** | **< 20 KB** |

---

## Future Enhancements (V2+)

- Document sharing with other users
- Collaborative group borrowing
- Advanced credit scoring (ML/AI)
- SMS notifications
- USSD support
- Mobile app (iOS/Android)
- Loan repayment tracking
- Transaction history export
- Advanced analytics
- Multi-language support
- Team/organization accounts

---

**Document Version**: 1.0
**Last Updated**: 2025-10-21
**Status**: Implementation Complete - Ready for Feature Development
