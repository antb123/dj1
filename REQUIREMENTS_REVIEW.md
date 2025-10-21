# Micro-Lending App Requirements Review

## 1. Snapshot
- **Audience**: Business stakeholders validating scope and developers planning implementation
- **Objective**: Deliver a mobile-first Django web app that allows low-bandwidth users to authenticate via WhatsApp OTP, complete KYC, understand their borrowing power, and request loans.
- **Primary Users**: Borrowers using feature phones or low-cost Android devices; internal administrators leveraging Django admin.

## 2. Guiding Goals
- Launch an MVP that works reliably on lightweight mobile browsers (<20 KB page weight, minimal JavaScript).
- Ensure KYC capture meets regulatory expectations while remaining low friction for borrowers.
- Provide transparent scoring and borrowing limits, including clear fees and required actions to unlock higher levels.
- Keep administration inside Django admin; no custom back-office build for this phase.

## 3. Experience Overview
1. User enters phone number and receives a WhatsApp OTP.
2. After OTP verification, user lands on a mobile dashboard showing KYC state, score, borrowing power, invite link, and required next actions.
3. User completes questionnaire (10 questions) to unlock KYC Level 1 and Ltd borrowing.
4. User optionally uploads supporting documents to earn KYC Level 2 and higher limit.
5. User increases score by inviting others or uploading phone bill evidence.
6. User requests a loan; system records transaction, applies configurable fee, and routes to admin for approval.
7. Admin reviews KYC and borrowing transactions inside Django admin.

## 4. Functional Requirements

### 4.1 Authentication & Access
- **Business Need**: Borrowers authenticate with OTP via WhatsApp; administrators continue to use Django admin credentials.
- **User Story**: As a borrower, I want to sign up and log in with my phone number so I can access the lending dashboard without remembering a password.
- **Acceptance Criteria**:
  - Borrower enters phone number, receives OTP via WhatsApp, and can request a resend after expiry.
  - OTP codes expire after 5 minutes and only 3 attempts are permitted before reissuing.
  - Successful verification creates or loads a `User` keyed by `phone_number`; password remains unusable.
  - Sessions time out per Django defaults; logout ends session.
  - Admin accounts remain accessible via `/admin/` using Django's default authentication.
- **Technical Notes**:
  - Integrate Twilio WhatsApp API (or configurable provider) for OTP delivery.
  - Store OTP metadata (code, expiry, attempts, phone number, is_used flag).
  - Capture WhatsApp opt-in status where required by provider policies.

### 4.2 Dashboard (Post-Login)
- **Business Need**: Single mobile-friendly page summarizing eligibility, score, and next steps.
- **Data Elements**:
  - `kyc_level` (0 none, 1 level 1, 2 level 2).
  - `score` (integer).
  - `borrow_limit.available_borrow`, `borrow_limit.max_borrow_amount`, `borrow_limit.is_locked`.
  - `aid_recipient` flag (default `True`).
  - `whatsapp_number` display (masked for privacy if desired).
- **UI Rules**:
  - Layout optimized for screens <= 480px wide; inline CSS, no heavy frameworks.
  - Buttons trigger server navigations; JavaScript limited to progressive enhancement (optional Ajax).
  - Borrow card stays locked, showing required action message until questionnaire completion.
  - Provide CTA tiles: `Complete Questionnaire`, `Invite via WhatsApp`, `Upload Phone Bill`, `Borrow Money`.
  - Invitation action opens native WhatsApp share intent with referral link when available.
- **Acceptance Criteria**:
  - Dashboard displays the current KYC level badge, score, borrowed history snippet, and outstanding docs.
  - Locked states show explicit messaging and disable navigation until prerequisites met.
  - Aid recipient flag shown and editable (future phase) via settings or support request.

### 4.3 KYC Levels
- **Level 1 (Questionnaire)**:
  - Unlock condition: all 10 questionnaire answers submitted, unique identifier generated (`phone_number + date_of_birth + id_number`).
  - Upon completion, set `kyc_level = 1`, award configured score bonus, unlock initial borrow limit (default 20 units).
- **Level 2 (Document Upload)**:
  - Required uploads: business registration proof, electricity bill (images or PDFs, max size configurable, e.g., 5 MB).
  - Admin verification required before setting `kyc_level = 2` and updating borrow limit/score per rules.
- **Administrative Workflow**:
  - Django admin list views for incomplete/awaiting verification profiles.
  - Ability to approve/reject documents, add notes, and record verified timestamp/user.

### 4.4 Questionnaire Capture
- **Question Set** (always presented in order):
  1. "Say your full name as on your ID. (You can also type.)"
  2. "Date of birth. Use keypad: DDMMYYYY."
  3. "City or village where you live. (You can say nearest market or landmark.)"
  4. "Mobile money number. Use keypad."
  5. "ID type. Say: national ID, voter card, passport, or other."
  6. "ID number. Use keypad."
  7. "You have a business? Press 1 Yes, 2 No."
  8. "Are you the only owner? Press 1 Yes, 2 No."
  9. "What do you do or sell? One sentence."
  10. "Loan purpose in one sentence."
- **UX Expectations**:
  - One lightweight page per question (or a single form with show/hide) with auto-save.
  - Support text input; optional audio recording can be captured for future voice-to-text but not required for MVP.
  - Validation includes required fields, DOB format, mobile money pattern, and accepted ID type values.
  - Allow editing answers before final submission; once submitted, changes require admin review.
- **Data Model**:
  - `KYCProfile` holds aggregated fields, timestamps for Level 1/2 completion, and `unique_identifier` property.
  - `QuestionnaireResponse` stores individual question index, text, answer, and `answered_at` timestamp.

### 4.5 Scoring
- **Score Drivers**:
  - KYC Level 1 completion (automatic award, configurable points).
  - KYC Level 2 verification (additional points after admin approval).
  - Successful referrals (invite accepted and verified new borrower).
  - Verified phone bill uploads.
  - Admin manual adjustments.
- **UI Requirements**:
  - Score card explains current score, history link, and available actions to increase score.
  - History page/table (future iteration) lists `ScoreLog` entries.
- **Acceptance Criteria**:
  - Score recalculated atomically when awarding points and persisted to `User.score`.
  - Each change recorded in `ScoreLog` with previous/new values and reason.
  - Referral codes unique per referrer; invitation link deep-links to OTP flow with referral metadata.
  - Handled by a Django Managmeent command that can be run on a schedule (cron or other)
   
### 4.6 Borrowing Flow
- **Preconditions**: `BorrowLimit.is_locked = False`, `available_borrow > 0`.
- **Borrow Request**:
  - User selects amount up to `available_borrow`; default limit 20 until scoring rules update.
  - Fee (percentage from `settings.BORROW_FEE_PERCENT`) shown before confirmation.
  - Confirmation screen summarises amount requested, fee, total debit, and repayment reminder.
  - Submission creates `BorrowTransaction` with `status = pending`, records `amount_before`, `amount_requested`, `borrow_fee`, `amount_debit`, `amount_after` (calculated), and timestamps.
- **Post-Request Handling**:
  - Borrow limit `available_borrow` reduced immediately or upon admin approval (define rule—default: deduct on approval).
  - Admin approves/declines in Django admin; approval sets `processed = True`, `status = approved`, `processed_at` timestamp.
  - Rejections restore available amount automatically.
  - Repayments recorded via `BorrowRepayment` linked back to transaction; once paid, status updates to `repaid`.
- **Notifications**: optional WhatsApp messages for approval or repayment reminders (out of scope for MVP but capture hooks).

### 4.7 Administration
- Operate entirely inside Django admin with tailored list filters for:
  - Pending KYC Level 2 documents.
  - Pending borrow transactions.
  - Referral approvals or fraud checks.
  - Score adjustments and audit logs.
- Admin actions to resend OTP manually are out of MVP scope.
- Ensure audit trail of admin user performing approvals.

## 5. Data & Integration Notes
- **Core Tables**: `User`, `WhatsAppUser`, `OTP`, `KYCProfile`, `QuestionnaireResponse`, `KYCDocument`, `ScoreLog`, `PhoneBillUpload`, `Referral`, `ScoreRule`, `BorrowLimit`, `BorrowTransaction`, `BorrowRepayment`.
- **Unique Identifier**: `whatsapp_number + date_of_birth + id_number` stored on `KYCProfile` and enforced unique (use DB constraint to prevent duplicates).
- **File Storage**: Local filesystem for dev, S3-compatible for production; enforce max upload size and allowed MIME types.
- **Settings Hooks**: expose Twilio credentials, OTP validity, borrow fee percent, referral points, phone bill points, maximum upload sizes, and allowed origin countries via environment variables.
- **Security**: rate-limit OTP requests per phone/IP; log suspicious attempts; ensure OTP codes hashed at rest if compliance requires.

## 6. Non-Functional Requirements
- **Performance**: Render HTML pages < 200 ms server time; total asset size < 20 KB per page where possible.
- **Accessibility**: WCAG AA-friendly color contrast, text size >= 14px, keyboard navigation supported.
- **Localization**: English copy for MVP with hooks for future translation.
- **Availability**: Target 99% uptime for MVP; schedule Twilio monitoring.
- **Compliance**: Store personal data in encrypted rest storage; log consent (`Consent. 'I agree to electronic verification and credit checks.'`).

## 7. Open Questions & Assumptions
1. Confirm Twilio (or alternative) WhatsApp Business API approval and messaging templates.
2. Determine whether questionnaire supports audio capture in MVP or text only.
3. Clarify currency and base borrowing unit (e.g., USD, CFA, NGN) for limits and fees.
4. Define repayment workflow deadlines and reminders.
5. Decide if borrow limit reduces immediately (on request) or after admin approval.
6. Establish regulatory requirements for document retention and consent language per target country.

## 8. Phasing Recommendation
- **Phase 1**: OTP auth, dashboard shell, questionnaire submission, KYC Level 1 unlock, initial borrow request recording (admin manual processing).
- **Phase 2**: Document upload + admin verification, score history, referral link, phone bill uploads.
- **Phase 3**: Notifications, repayment automation, analytics, localization.

## 9. Appendix: Questionnaire Validation Rules
| # | Question | Required | Validation |
|---|----------|----------|------------|
| 1 | Full legal name | Yes | Alphabetic plus spaces; 3-120 chars |
| 2 | Date of birth | Yes | `DDMMYYYY`; convertible to valid date; age >= 18 |
| 3 | City/village | Yes | Text 2-120 chars |
| 4 | Mobile money number | Yes | Country-specific regex; up to 15 digits |
| 5 | ID type | Yes | One of: national_id, voter_card, passport, other |
| 6 | ID number | Yes | 4-30 alphanumeric chars |
| 7 | Business owner? | Yes | `1` for yes, `2` for no |
| 8 | Sole owner? | Yes | `1` or `2`; skip logic if Q7 = No (optional) |
| 9 | Business description | Yes | 5-160 chars |
|10 | Loan purpose | Yes | 5-160 chars |

