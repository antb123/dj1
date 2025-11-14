# Frontend Customization Implementation Plan - FreedomPayWallet

## Overview
This ticket provides step-by-step instructions to customize colors, logos, and fonts for the Stellar Disbursement Platform Frontend with FreedomPayWallet branding.

**Repository**: https://github.com/stellar/stellar-disbursement-platform-frontend

**Tech Stack**: React + TypeScript, Vite, SCSS, @stellar/design-system, Docker + Nginx

**Build Output**: `/build` directory → Docker image → Nginx

---

## Prerequisites

- [ ] Access to the frontend repository
- [ ] Node.js 22.x and Yarn installed locally
- [ ] Docker installed for building and testing
- [ ] Custom brand assets prepared:
  - Logo files (SVG, PNG in multiple sizes)
  - Font files (WOFF2 format recommended) or Google Fonts selection
  - Brand color palette (hex codes)

---

## Phase 1: Preparation & Asset Collection

### Step 1.1: Prepare Logo Assets - FreedomPayWallet Branding

FreedomPayWallet logo assets to be used:

| File Purpose | URL/Source | Format | Usage |
|--------------|------------|--------|-------|
| Main Logo | https://freedompaywallet.com/wp-content/uploads/2025/05/FPW_WHITE_NEW_LOGO.png | PNG | Header, main app logo |
| Favicon 32x32 | https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-32x32.png | PNG | Browser favicon |
| Favicon 192x192 | https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-192x192.png | PNG | PWA icon small |
| Apple Touch Icon | https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-180x180.png | PNG | iOS home screen |
| MS Tile | https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-270x270.png | PNG | Windows tile |

**Download Assets**:
```bash
# Create assets directory
mkdir -p public/fpw-logos
mkdir -p src/assets/fpw

# Download logos using curl or wget
curl -o public/fpw-logos/fpw-main-logo.png "https://freedompaywallet.com/wp-content/uploads/2025/05/FPW_WHITE_NEW_LOGO.png"
curl -o public/fpw-logos/favicon-32x32.png "https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-32x32.png"
curl -o public/fpw-logos/favicon-192x192.png "https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-192x192.png"
curl -o public/fpw-logos/apple-touch-icon.png "https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-180x180.png"
curl -o public/fpw-logos/mstile-270x270.png "https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-270x270.png"
```

### Step 1.2: Prepare Font Files - FreedomPayWallet Fonts

**FreedomPayWallet uses Google Fonts**:
- **Primary Font**: Inter (weights: 400, 600)
- **Secondary Font**: Plus Jakarta Sans (weight: 600)

**Google Fonts URL**:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css?family=Inter:400,600|Plus+Jakarta+Sans:600&display=fallback"
  rel="stylesheet"
/>
```

### Step 1.3: Define Brand Colors - FreedomPayWallet Palette

Analyze FreedomPayWallet site and define color palette:

```scss
// FreedomPayWallet Brand Colors (extract from site)
$fpw-primary: #YOUR_PRIMARY_COLOR;      // Main brand color
$fpw-secondary: #YOUR_SECONDARY_COLOR;  // Accent color
$fpw-success: #16A34A;                  // Green for success states
$fpw-error: #DC2626;                    // Red for error states
$fpw-warning: #F59E0B;                  // Amber for warnings
$fpw-info: #2563EB;                     // Blue for info

// Gray Scale
$fpw-gray-lightest: #FAFAFA;
$fpw-gray-light: #F5F5F5;
$fpw-gray-medium: #9E9E9E;
$fpw-gray-dark: #424242;
$fpw-gray-darkest: #1A1A1A;

// Text Colors
$fpw-text-primary: #212121;
$fpw-text-secondary: #616161;
$fpw-link: #2563EB;
```

### Step 1.4: Fork and Clone Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/stellar-disbursement-platform-frontend.git
cd stellar-disbursement-platform-frontend

# Create a feature branch
git checkout -b feature/fpw-branding

# Install dependencies
yarn install
```

---

## Phase 2: Font Customization - FreedomPayWallet Fonts

### Step 2.1: Update index.html with Google Fonts

**File**: [`index.html`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/index.html)

**Replace existing Google Fonts** with FreedomPayWallet fonts:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#YOUR_BRAND_COLOR" />
    <meta name="description" content="FreedomPayWallet - Secure Cryptocurrency Wallet" />

    <title>FreedomPayWallet</title>

    <!-- FreedomPayWallet Favicons -->
    <link rel="icon" href="https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-32x32.png" sizes="32x32" />
    <link rel="icon" href="https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-192x192.png" sizes="192x192" />
    <link rel="apple-touch-icon" href="https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-180x180.png" />
    <meta name="msapplication-TileImage" content="https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-270x270.png" />

    <!-- FreedomPayWallet Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css?family=Inter:400,600|Plus+Jakarta+Sans:600&display=fallback"
      rel="stylesheet"
    />

    <!-- FreedomPayWallet Custom CSS (Optional) -->
    <link
      rel="stylesheet"
      href="https://freedompaywallet.com/wp-content/uploads/elementor/css/post-9123.css?ver=1762183646"
      media="all"
    />

    <link rel="manifest" href="/manifest.json" />
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    <script type="module" src="/src/index.tsx"></script>
  </body>
</html>
```

**Files modified**:
- [`index.html`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/index.html)

### Step 2.2: Override Design System Font Variables

**File**: [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

**Add at the top of the file**:

```scss
@use "./styles-utils.scss" as *;

// ============================================
// FREEDOMPAYWALLET BRANDING: Font Overrides
// ============================================
:root {
  // FreedomPayWallet primary font: Inter
  --sds-ff-base: 'Inter', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;

  // FreedomPayWallet secondary font: Plus Jakarta Sans
  --fpw-ff-heading: 'Plus Jakarta Sans', 'Inter', sans-serif;

  // Font weights (Inter: 400, 600; Plus Jakarta Sans: 600)
  --sds-fw-regular: 400;
  --sds-fw-semi-bold: 600;
  --sds-fw-bold: 600;
}

// Apply to body
body {
  font-family: var(--sds-ff-base);
  font-size: pxToRem(14px);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

// Use Plus Jakarta Sans for headings
h1, h2, h3, h4, h5, h6, .heading {
  font-family: var(--fpw-ff-heading);
  font-weight: var(--sds-fw-semi-bold);
}
// ============================================
// END FREEDOMPAYWALLET BRANDING
// ============================================
```

**Files modified**:
- [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

---

## Phase 3: Logo Customization - FreedomPayWallet

### Step 3.1: Update PWA Manifest with FreedomPayWallet Branding

**File**: [`public/manifest.json`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/manifest.json)

```json
{
  "short_name": "FreedomPay",
  "name": "FreedomPayWallet - Secure Crypto Wallet",
  "icons": [
    {
      "src": "https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-192x192.png",
      "type": "image/png",
      "sizes": "192x192",
      "purpose": "any maskable"
    },
    {
      "src": "https://freedompaywallet.com/wp-content/uploads/2025/09/cropped-FPW_Logo_WhiteGap_Favicon-6-270x270.png",
      "type": "image/png",
      "sizes": "270x270",
      "purpose": "any maskable"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#YOUR_BRAND_COLOR",
  "background_color": "#ffffff",
  "description": "FreedomPayWallet - Your gateway to secure cryptocurrency transactions"
}
```

**Files modified**:
- [`public/manifest.json`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/manifest.json)

### Step 3.2: Create Logo Component with FreedomPayWallet Logo

**File**: Create `src/components/Logo.tsx`

```typescript
import React from 'react';

interface LogoProps {
  width?: number;
  height?: number;
  className?: string;
  variant?: 'white' | 'dark';
}

export const Logo: React.FC<LogoProps> = ({
  width = 200,
  height = 60,
  className = '',
  variant = 'white'
}) => {
  const logoUrl = variant === 'white'
    ? 'https://freedompaywallet.com/wp-content/uploads/2025/05/FPW_WHITE_NEW_LOGO.png'
    : 'https://freedompaywallet.com/wp-content/uploads/2025/05/FPW_WHITE_NEW_LOGO.png'; // Replace with dark variant if available

  return (
    <img
      src={logoUrl}
      alt="FreedomPayWallet Logo"
      width={width}
      height={height}
      className={`fpw-logo ${className}`}
      style={{ maxWidth: '100%', height: 'auto' }}
      loading="lazy"
    />
  );
};

export default Logo;
```

**Files created**:
- [`src/components/Logo.tsx`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/src/components)

---

## Phase 4: Color and Theme Customization

### Step 4.1: Override Design System Color Variables

**File**: [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

**Add color overrides** (analyze FreedomPayWallet site and extract colors):

```scss
:root {
  // ... font variables from earlier ...

  // ============================================
  // FREEDOMPAYWALLET BRANDING: Color Overrides
  // ============================================

  // Primary brand colors (extract from freedompaywallet.com)
  --sds-clr-primary: #YOUR_PRIMARY_COLOR;       // FPW primary brand color
  --sds-clr-primary-dark: #YOUR_PRIMARY_DARK;   // Darker shade
  --sds-clr-primary-light: #YOUR_PRIMARY_LIGHT; // Lighter shade

  // Secondary accent
  --fpw-accent: #YOUR_ACCENT_COLOR;

  // Gray scale
  --sds-clr-gray-01: #FAFAFA;
  --sds-clr-gray-02: #F5F5F5;
  --sds-clr-gray-03: #EEEEEE;
  --sds-clr-gray-04: #E0E0E0;
  --sds-clr-gray-05: #BDBDBD;
  --sds-clr-gray-06: #9E9E9E;
  --sds-clr-gray-07: #757575;
  --sds-clr-gray-08: #616161;
  --sds-clr-gray-09: #424242;
  --sds-clr-gray-10: #303030;
  --sds-clr-gray-11: #212121;
  --sds-clr-gray-12: #1A1A1A;

  // Semantic colors
  --sds-clr-red-05: #FEE2E2;
  --sds-clr-red-10: #DC2626;
  --sds-clr-red-15: #991B1B;

  --sds-clr-green-05: #D4EDDA;
  --sds-clr-green-10: #16A34A;
  --sds-clr-green-15: #166534;

  --sds-clr-amber-05: #FEF3C7;
  --sds-clr-amber-10: #F59E0B;
  --sds-clr-amber-15: #92400E;

  --sds-clr-blue-05: #DBEAFE;
  --sds-clr-blue-10: #2563EB;
  --sds-clr-blue-15: #1E3A8A;

  // ============================================
  // END FREEDOMPAYWALLET BRANDING
  // ============================================
}
```

**Files modified**:
- [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

---

## Phase 5: Forward Compatibility Setup

### Step 5.1: Create Override Pattern

To ensure forward compatibility with Stellar Design System updates, create a dedicated override file:

**File**: Create `src/styles/brand-overrides.scss`

```scss
// ============================================
// BRAND OVERRIDES - FreedomPayWallet
// This file contains all custom branding that overrides
// the Stellar Design System defaults.
//
// When updating @stellar/design-system, review this file
// to ensure overrides still work as expected.
// ============================================

:root {
  // Import from brand configuration
  // Fonts
  --sds-ff-base: var(--brand-font-base);
  --sds-ff-monospace: var(--brand-font-mono);

  // Colors
  --sds-clr-primary: var(--brand-color-primary);
  // ... other overrides
}

// Brand-specific custom properties
:root {
  // Define brand tokens
  --brand-font-base: 'Inter', -apple-system, sans-serif;
  --brand-font-heading: 'Plus Jakarta Sans', 'Inter', sans-serif;
  --brand-font-mono: 'Fira Code', 'Inconsolata', monospace;

  --brand-color-primary: #YOUR_COLOR;
  --brand-color-success: #YOUR_SUCCESS;
  --brand-color-error: #YOUR_ERROR;
  --brand-color-warning: #YOUR_WARNING;
  --brand-color-info: #YOUR_INFO;
}
```

**File**: Update [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

```scss
@use "./styles-utils.scss" as *;
@use "./brand-overrides.scss"; // ← Import brand overrides

// Rest of the file...
```

**Files created**:
- `src/styles/brand-overrides.scss`

**Files modified**:
- [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

### Step 5.2: Add Git Attributes for Merge Strategy

**File**: Create `.gitattributes` in repository root

```
# Custom branding files - prefer ours in merges
src/styles/brand-overrides.scss merge=ours
src/assets/app-logo.* merge=ours
src/components/Logo.tsx merge=ours
public/favicon.ico merge=binary
public/icon.svg merge=ours
public/apple-touch-icon.png merge=binary
public/icon-*.png merge=binary
public/manifest.json merge=ours
CUSTOMIZATION_NOTES.md merge=ours

# Standard text files
*.md text
*.scss text
*.tsx text
*.ts text
*.json text
```

**Files created**:
- `.gitattributes` (new file)

### Step 5.3: Configure Dependabot to Monitor Design System

**File**: Create `.github/dependabot.yml` (if it doesn't exist)

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
    # Group design system updates separately
    groups:
      stellar-design-system:
        patterns:
          - "@stellar/design-system"
    # Don't auto-merge design system updates
    open-pull-requests-limit: 10
```

**Files created or modified**:
- [`.github/dependabot.yml`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/.github)

---

## Phase 6: Docker Build Configuration

### Step 6.1: Verify Dockerfile Handles Assets

**File**: [`Dockerfile`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/Dockerfile)

**No changes needed** - The current multi-stage build already:
- Copies all source files (including `public/` and `src/assets/`)
- Runs `yarn build` which processes assets via Vite
- Copies the `/app/build/` directory to nginx

**Verify the build process**:
```dockerfile
# Build stage already includes:
COPY . .                          # ← Copies all source including custom assets
RUN yarn build                    # ← Vite processes fonts, logos, styles

# Runtime stage already includes:
COPY --from=build /app/build/ /usr/share/nginx/html/  # ← Serves built assets
```

**Files verified** (no modifications needed):
- [`Dockerfile`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/Dockerfile)

### Step 6.2: Enhanced Nginx Configuration (Optional)

**Create**: `nginx-fpw.conf`

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html index.htm;

    # Enable gzip compression
    gzip on;
    gzip_static on;
    gzip_vary on;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript
               text/xml application/xml application/xml+rss text/javascript
               image/svg+xml;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location ~* \.(css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA routing
    location / {
        try_files $uri /index.html index.htm;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # API proxy (if needed)
    location /api/ {
        proxy_pass https://api.freedompaywallet.com/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Files optionally created**:
- `nginx-fpw.conf`

### Step 6.3: Configure Environment Variables for Branding

**File**: Create `.env.example` for documentation

```env
# Application Configuration
VITE_APP_NAME=FreedomPayWallet
VITE_COMPANY_NAME=FreedomPay
VITE_API_URL=https://api.freedompaywallet.com
VITE_HORIZON_URL=https://horizon.stellar.org

# Branding
VITE_PRIMARY_COLOR=#YOUR_COLOR

# Feature Flags
VITE_ENABLE_SINGLE_TENANT_MODE=false
VITE_USE_SSO=false

# Analytics (optional)
VITE_GA_TRACKING_ID=
```

**Files created**:
- `.env.example`

---

## Phase 7: Build and Test

### Step 7.1: Test Local Development Build

```bash
# Install dependencies
yarn install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start development server
yarn dev

# Open browser to http://localhost:5173
# Verify:
# ✓ FreedomPayWallet logo loads
# ✓ Inter and Plus Jakarta Sans fonts render
# ✓ Colors match brand palette
# ✓ Favicons display correctly
```

### Step 7.2: Test Production Build Locally

```bash
# Build for production
yarn build

# Preview production build
yarn preview

# Verify:
# - All assets are in build/ directory
# - Fonts are in build/assets/
# - Logos are properly referenced
# - Styles are compiled correctly
```

### Step 7.3: Build Docker Image

```bash
# Build Docker image
docker build -t fpw-frontend:latest .

# Verify build completed
docker images | grep fpw-frontend
```

### Step 7.4: Test Docker Container

```bash
# Run container
docker run -d -p 8080:80 --name fpw-frontend-test fpw-frontend:latest

# Test in browser
open http://localhost:8080

# Verify:
# ✓ Application loads with FreedomPayWallet branding
# ✓ Fonts render correctly (Inter, Plus Jakarta Sans)
# ✓ Logo displays properly
# ✓ All routes work

# Stop and remove
docker stop fpw-frontend-test
docker rm fpw-frontend-test
```

### Step 7.5: Validate Assets in Built Container

```bash
# Run container with shell access
docker run -it --rm fpw-frontend:latest sh

# Inside container, verify assets exist:
ls -la /usr/share/nginx/html/
ls -la /usr/share/nginx/html/assets/

# Verify key files:
# - index.html
# - manifest.json
# - assets/ directory with hashed files
```

---

## Phase 8: Deployment

### Step 8.1: Production Environment Variables

```env
# Production .env
VITE_APP_NAME=FreedomPayWallet
VITE_API_URL=https://api.freedompaywallet.com
VITE_HORIZON_URL=https://horizon.stellar.org
```

### Step 8.2: Tag and Push Docker Image

```bash
# Tag for your registry
docker tag fpw-frontend:latest your-registry.com/fpw-frontend:v1.0.0
docker tag fpw-frontend:latest your-registry.com/fpw-frontend:latest

# Push to registry
docker push your-registry.com/fpw-frontend:v1.0.0
docker push your-registry.com/fpw-frontend:latest
```

### Step 8.3: Update Docker Compose (If Applicable)

**File**: Update your deployment's `docker-compose.yml`

```yaml
version: '3.8'

services:
  frontend:
    image: your-registry.com/fpw-frontend:latest
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=${API_URL}
    restart: unless-stopped
    networks:
      - sdp-network

networks:
  sdp-network:
    driver: bridge
```

### Step 8.4: Deploy to Production

```bash
# Pull latest image
docker-compose pull frontend

# Restart with new image
docker-compose up -d frontend

# Verify deployment
docker-compose ps
docker-compose logs frontend
```

---

## Phase 9: Validation and QA

### Step 9.1: Cross-Browser Testing

Test on:
- [ ] Chrome/Chromium (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

Verify:
- [ ] Fonts load and render correctly
- [ ] Logo displays at correct sizes
- [ ] Colors match brand palette
- [ ] Favicon shows in browser tab
- [ ] PWA install prompt works (mobile)

### Step 9.2: Performance Testing

```bash
# Use Lighthouse in Chrome DevTools
# Target scores:
# - Performance: >90
# - Accessibility: >90
# - Best Practices: >90
# - SEO: >90

# Check font loading performance
# - Fonts should load with font-display: swap
# - No FOIT (Flash of Invisible Text)
# - No layout shift from font loading
```

### Step 9.3: Accessibility Testing

- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 for normal text)
- [ ] Logo alt text is descriptive
- [ ] Text remains readable with custom fonts
- [ ] No accessibility regressions from customization

### Step 9.4: PWA Testing

```bash
# Chrome DevTools → Application tab
# Verify:
# - Manifest loads correctly
# - Icons display in all sizes
# - Theme color is applied
# - App can be installed
# - Service worker works (if applicable)
```

---

## Phase 10: Documentation and Handoff

### Step 10.1: Document Customizations

**File**: Create `CUSTOMIZATION_NOTES.md`

```markdown
# FreedomPayWallet Brand Customization Notes

This document tracks all branding customizations made to this fork of the Stellar Disbursement Platform Frontend.

## Customized Files

### Fonts
- `src/styles/styles.scss` - Font variable overrides
- `src/styles/brand-overrides.scss` - Centralized brand overrides
- `index.html` - Google Fonts imports (Inter, Plus Jakarta Sans)

### Logos
- `src/components/Logo.tsx` - Logo component
- `public/manifest.json` - PWA metadata
- `index.html` - Favicon references

### Colors
- `src/styles/styles.scss` - Color variable overrides
- `src/styles/brand-overrides.scss` - Brand color tokens

### Metadata
- `index.html` - Title, description, theme color
- `public/manifest.json` - App name, description, theme

## Brand Assets

### Fonts
- Primary: Inter (400, 600)
- Headings: Plus Jakarta Sans (600)
- Source: Google Fonts

### Logos
- Main: https://freedompaywallet.com/wp-content/uploads/2025/05/FPW_WHITE_NEW_LOGO.png
- Favicons: Multiple sizes from freedompaywallet.com

### Colors
- Primary: #______
- Success: #16A34A
- Error: #DC2626
- Warning: #F59E0B
- Info: #2563EB

## Forward Compatibility Strategy

All customizations use CSS custom property overrides, allowing the underlying Stellar Design System to be updated without conflicts.

### Merging Upstream Changes

```bash
git remote add upstream https://github.com/stellar/stellar-disbursement-platform-frontend.git
git fetch upstream
git merge upstream/main
# Resolve conflicts, prioritizing our branding customizations
```

## Last Updated
[Date] - Initial FreedomPayWallet branding implementation
```

**Files created**:
- `CUSTOMIZATION_NOTES.md`

### Step 10.2: Create Maintenance Checklist

**File**: Create `MAINTENANCE.md`

```markdown
# Maintenance Checklist

## Monthly Tasks
- [ ] Check for @stellar/design-system updates
- [ ] Review dependabot PRs
- [ ] Test branding on latest browsers

## Quarterly Tasks
- [ ] Merge upstream changes from stellar/stellar-disbursement-platform-frontend
- [ ] Review and update color overrides if needed
- [ ] Verify font loading performance
- [ ] Update Docker base images

## Annual Tasks
- [ ] Review and refresh brand assets
- [ ] Audit accessibility compliance
- [ ] Performance audit
- [ ] Review font licenses

## Updating Design System

When updating @stellar/design-system:

1. Check release notes for breaking changes
2. Test locally: `yarn upgrade @stellar/design-system`
3. Review `src/styles/brand-overrides.scss` for conflicts
4. Test all pages visually
5. Run full test suite
6. Build Docker image and test
7. Deploy to staging first
```

**Files created**:
- `MAINTENANCE.md`

### Step 10.3: Version and Tag

```bash
# Commit all changes
git add .
git commit -m "feat: implement FreedomPayWallet branding (fonts, logos, colors)"

# Create annotated tag
git tag -a v1.0.0-fpw -m "FreedomPayWallet branded version with custom fonts, logos, and colors"

# Push commits and tags
git push origin feature/fpw-branding
git push origin v1.0.0-fpw
```

---

## Summary of Modified Files

### Created Files
- [ ] `src/components/Logo.tsx` - FreedomPayWallet logo component
- [ ] `src/styles/brand-overrides.scss` - Centralized overrides
- [ ] `CUSTOMIZATION_NOTES.md` - Customization documentation
- [ ] `MAINTENANCE.md` - Maintenance procedures
- [ ] `.env.example` - Environment variable template
- [ ] `.gitattributes` - Merge strategy for brand files
- [ ] `nginx-fpw.conf` - Enhanced nginx config (optional)

### Modified Files
- [ ] [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss) - Font and color overrides
- [ ] [`index.html`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/index.html) - FPW fonts, logos, meta tags
- [ ] [`public/manifest.json`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/manifest.json) - App metadata
- [ ] `README.md` - Add customization section

---

## Forward Compatibility Strategy

### Design Principles

1. **CSS Custom Property Overrides**: All styling changes use CSS variable overrides rather than modifying component styles directly
2. **Separate Override Files**: Brand customizations are isolated in dedicated files
3. **Git Attributes**: Merge strategy preserves brand files during upstream updates
4. **Documentation**: All changes are documented for future maintenance
5. **Minimal Core Changes**: Only essential files are modified

### Merging Upstream Updates

```bash
# Add upstream remote (one time)
git remote add upstream https://github.com/stellar/stellar-disbursement-platform-frontend.git

# Fetch upstream changes
git fetch upstream

# Merge upstream main
git checkout main
git merge upstream/main

# Resolve conflicts
# - For brand files: keep "ours" (your changes)
# - For core files: review carefully, preserve brand overrides

# Test after merge
yarn install
yarn build
docker build -t fpw-frontend:test .
docker run -d -p 8080:80 fpw-frontend:test
# Verify branding still works

# If tests pass
git push origin main
```

### Safe Update Process

1. Create update branch: `git checkout -b update/upstream-YYYY-MM-DD`
2. Merge upstream: `git merge upstream/main`
3. Resolve conflicts (prioritize brand files)
4. Test locally: `yarn dev`
5. Test build: `yarn build && yarn preview`
6. Test Docker: Build and run container
7. QA all branding elements
8. Merge to main only after full validation

---

## Estimated Timeline

| Phase | Estimated Time | Dependencies |
|-------|---------------|--------------|
| 1. Preparation | 2-4 hours | Asset creation |
| 2. Font Customization | 1-2 hours | Phase 1 |
| 3. Logo Customization | 1-2 hours | Phase 1 |
| 4. Color Customization | 1-2 hours | - |
| 5. Forward Compatibility | 1 hour | - |
| 6. Docker Configuration | 1 hour | - |
| 7. Build and Test | 2-3 hours | Phases 2-6 |
| 8. Deployment | 1-2 hours | Phase 7, infrastructure |
| 9. Validation & QA | 2-4 hours | Phase 8 |
| 10. Documentation | 1-2 hours | All phases |
| **Total** | **13-23 hours** | - |

---

## Support and Resources

- **Stellar Design System**: https://github.com/stellar/stellar-design-system
- **Vite Documentation**: https://vitejs.dev/
- **Docker Documentation**: https://docs.docker.com/
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **Google Fonts**: https://fonts.google.com/
- **Lighthouse**: https://developers.google.com/web/tools/lighthouse

### FreedomPayWallet Resources
- **Website**: https://freedompaywallet.com
- **Logo Assets**: See Step 1.1
- **Fonts**: Google Fonts (Inter, Plus Jakarta Sans)
- **Custom CSS**: https://freedompaywallet.com/wp-content/uploads/elementor/css/post-9123.css

---

## Acceptance Criteria

- [ ] FreedomPayWallet logo displays in all sizes
- [ ] Inter (400, 600) and Plus Jakarta Sans (600) fonts load
- [ ] Colors match brand palette throughout application
- [ ] Favicon and PWA icons match brand
- [ ] PWA manifest reflects custom branding
- [ ] Docker image builds successfully
- [ ] Application runs correctly in Docker container
- [ ] All routes work (SPA routing intact)
- [ ] Performance scores remain high (Lighthouse >90)
- [ ] Accessibility maintained (WCAG 2.1 AA)
- [ ] Documentation complete
- [ ] Forward compatibility strategy implemented
- [ ] QA passed on all target browsers
- [ ] Deployed to production successfully

---

**Ticket Created By**: Claude
**Date**: 2025-11-14
**Target Completion**: [Set based on sprint planning]
