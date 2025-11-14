# Frontend Customization Implementation Plan

## Overview
This ticket provides step-by-step instructions to customize colors, logos, and fonts for the Stellar Disbursement Platform Frontend while maintaining forward compatibility with future updates.

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

### Step 1.1: Prepare Logo Assets

Create the following logo files with your branding:

| File Purpose | Size | Format | Naming |
|--------------|------|--------|--------|
| App Icon SVG | Scalable | SVG | `icon.svg` |
| Favicon | 32x32 | ICO | `favicon.ico` |
| iOS Icon | 180x180 | PNG | `apple-touch-icon.png` |
| PWA Icon Small | 192x192 | PNG | `icon-192.png` |
| PWA Icon Large | 512x512 | PNG | `icon-512.png` |
| App Logo (Header) | Variable | SVG preferred | `app-logo.svg` |

**Tools for preparation**:
- SVG: Use Figma, Adobe Illustrator, or Inkscape
- Resize PNGs: https://squoosh.app or ImageMagick
- ICO converter: https://www.icoconverter.com
- Optimize SVGs: https://jakearchibald.github.io/svgomg/

### Step 1.2: Prepare Font Files

**Option A: Using Google Fonts (Recommended for simplicity)**
1. Select fonts at https://fonts.google.com
2. Note the font family names and weights needed
3. Copy the Google Fonts `<link>` embed code

**Option B: Using Custom Fonts (Better for branding)**
1. Obtain font files in WOFF2 format (best compression)
2. Ensure you have licenses for web use
3. Prepare font files for Regular (400), Medium (500), Semi-Bold (600), Bold (700) weights
4. Naming convention: `YourFont-Regular.woff2`, `YourFont-Bold.woff2`, etc.

### Step 1.3: Define Brand Colors

Document your brand color palette:

```
Primary Color: #______
Secondary Color: #______
Success Color: #______
Error Color: #______
Warning Color: #______
Info Color: #______

Gray Scale:
- Lightest: #______
- Light: #______
- Medium: #______
- Dark: #______
- Darkest: #______

Text:
- Primary Text: #______
- Secondary Text: #______
- Link Color: #______
```

### Step 1.4: Fork and Clone Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/stellar-disbursement-platform-frontend.git
cd stellar-disbursement-platform-frontend

# Create a feature branch
git checkout -b feature/custom-branding

# Install dependencies
yarn install
```

---

## Phase 2: Font Customization

### Step 2.1: Add Font Files (If Using Custom Fonts)

**File**: Create directory and add fonts

```bash
# Create fonts directory in public
mkdir -p public/fonts

# Copy your font files
cp /path/to/your/fonts/*.woff2 public/fonts/
```

**Files affected**:
- [`public/fonts/`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/public) (new directory)

### Step 2.2: Create Font Declarations

**File**: Create `src/styles/fonts.scss`

```bash
# Create new file
touch src/styles/fonts.scss
```

**Content for `src/styles/fonts.scss`**:

**If using custom fonts**:
```scss
// Custom font declarations
@font-face {
  font-family: 'YourBrandFont';
  src: url('/fonts/YourBrandFont-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'YourBrandFont';
  src: url('/fonts/YourBrandFont-Medium.woff2') format('woff2');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'YourBrandFont';
  src: url('/fonts/YourBrandFont-SemiBold.woff2') format('woff2');
  font-weight: 600;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'YourBrandFont';
  src: url('/fonts/YourBrandFont-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
```

**If using Google Fonts**:
```scss
// Google Fonts will be imported in index.html
// This file can be empty or contain fallback configurations
```

**Files created**:
- [`src/styles/fonts.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/src/styles) (new file)

### Step 2.3: Update index.html for Google Fonts (If Using)

**File**: [`index.html`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/index.html)

**Current Google Fonts import** (lines ~7-12):
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inconsolata:wght@400;500;600&display=swap"
  rel="stylesheet"
/>
```

**Replace with your Google Fonts**:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;500;600;700&display=swap"
  rel="stylesheet"
/>
```

**Files modified**:
- [`index.html`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/index.html)

### Step 2.4: Override Design System Font Variables

**File**: [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

**Add at the top of the file** (after `@use` statements):

```scss
@use "./styles-utils.scss" as *;
@use "./fonts.scss"; // Import custom fonts

// ============================================
// CUSTOM BRANDING: Font Overrides
// ============================================
:root {
  // Override Stellar Design System base font
  --sds-ff-base: 'YourBrandFont', 'Inter', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;

  // Override monospace font (for code/technical content)
  --sds-ff-monospace: 'Fira Code', 'Inconsolata', 'Courier New', monospace;

  // Font weights (align with your font's available weights)
  --sds-fw-regular: 400;
  --sds-fw-medium: 500;
  --sds-fw-semi-bold: 600;
  --sds-fw-bold: 700;
}

// Apply to body
body {
  font-family: var(--sds-ff-base);
  font-size: pxToRem(14px);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
// ============================================
// END CUSTOM BRANDING
// ============================================
```

**Files modified**:
- [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

---

## Phase 3: Logo Customization

### Step 3.1: Replace Favicon and App Icons

**Files**: [`public/`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/public) directory

```bash
# Backup originals
cp public/favicon.ico public/favicon.ico.original
cp public/icon.svg public/icon.svg.original
cp public/apple-touch-icon.png public/apple-touch-icon.png.original
cp public/icon-192.png public/icon-192.png.original
cp public/icon-512.png public/icon-512.png.original

# Replace with your branded icons
cp /path/to/your/branding/favicon.ico public/
cp /path/to/your/branding/icon.svg public/
cp /path/to/your/branding/apple-touch-icon.png public/
cp /path/to/your/branding/icon-192.png public/
cp /path/to/your/branding/icon-512.png public/
```

**Files modified**:
- [`public/favicon.ico`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/favicon.ico)
- [`public/icon.svg`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/icon.svg)
- [`public/apple-touch-icon.png`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/apple-touch-icon.png)
- [`public/icon-192.png`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/icon-192.png)
- [`public/icon-512.png`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/icon-512.png)

### Step 3.2: Add Application Logo

**File**: Add to [`src/assets/`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/src/assets)

```bash
# Add your main application logo
cp /path/to/your/branding/app-logo.svg src/assets/
# or
cp /path/to/your/branding/app-logo.png src/assets/
```

**Files created**:
- [`src/assets/app-logo.svg`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/src/assets) (new file)

### Step 3.3: Create Logo Component

**File**: Create `src/components/Logo.tsx`

```typescript
import appLogo from '@/assets/app-logo.svg'; // Adjust extension if using PNG

interface LogoProps {
  width?: number;
  height?: number;
  className?: string;
}

export const Logo = ({ width = 150, height = 50, className = '' }: LogoProps) => {
  return (
    <img
      src={appLogo}
      alt="Application Logo"
      width={width}
      height={height}
      className={className}
      style={{ maxWidth: '100%', height: 'auto' }}
    />
  );
};
```

**Files created**:
- [`src/components/Logo.tsx`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/src/components) (new file)

### Step 3.4: Update PWA Manifest

**File**: [`public/manifest.json`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/manifest.json)

**Update with your branding**:
```json
{
  "short_name": "YourApp",
  "name": "Your Application Name",
  "icons": [
    {
      "src": "icon-192.png",
      "type": "image/png",
      "sizes": "192x192",
      "purpose": "any maskable"
    },
    {
      "src": "icon-512.png",
      "type": "image/png",
      "sizes": "512x512",
      "purpose": "any maskable"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#YOUR_BRAND_COLOR",
  "background_color": "#ffffff",
  "description": "Your application description"
}
```

**Files modified**:
- [`public/manifest.json`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/manifest.json)

### Step 3.5: Update HTML Meta Tags

**File**: [`index.html`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/index.html)

**Update title and theme color**:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#YOUR_BRAND_COLOR" />
    <meta name="description" content="Your application description" />

    <!-- Update title -->
    <title>Your Application Name</title>

    <!-- Icons remain the same -->
    <link rel="icon" href="/favicon.ico" sizes="32x32" />
    <link rel="icon" href="/icon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/manifest.json" />

    <!-- Font imports... -->
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

---

## Phase 4: Color and Theme Customization

### Step 4.1: Override Design System Color Variables

**File**: [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

**Add color overrides** (in the `:root` block created earlier):

```scss
:root {
  // ... font variables from earlier ...

  // ============================================
  // CUSTOM BRANDING: Color Overrides
  // ============================================

  // Primary brand color
  --sds-clr-primary: #YOUR_PRIMARY_COLOR;
  --sds-clr-primary-dark: #YOUR_PRIMARY_DARK;
  --sds-clr-primary-light: #YOUR_PRIMARY_LIGHT;

  // Gray scale (01 = lightest, 12 = darkest)
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
  --sds-clr-red-05: #FEE2E2;    // Light red background
  --sds-clr-red-10: #DC2626;    // Error/danger
  --sds-clr-red-15: #991B1B;    // Dark red

  --sds-clr-green-05: #D4EDDA;  // Light green background
  --sds-clr-green-10: #16A34A;  // Success
  --sds-clr-green-15: #166534;  // Dark green

  --sds-clr-amber-05: #FEF3C7;  // Light amber background
  --sds-clr-amber-10: #F59E0B;  // Warning
  --sds-clr-amber-15: #92400E;  // Dark amber

  --sds-clr-blue-05: #DBEAFE;   // Light blue background
  --sds-clr-blue-10: #2563EB;   // Info
  --sds-clr-blue-15: #1E3A8A;   // Dark blue

  // Spacing (optional - adjust if needed)
  --sds-gap-xs: 4px;
  --sds-gap-sm: 8px;
  --sds-gap-md: 16px;
  --sds-gap-lg: 24px;
  --sds-gap-xl: 32px;
  --sds-gap-xxl: 48px;

  // Border radius (optional)
  --sds-radius-sm: 4px;
  --sds-radius-md: 8px;
  --sds-radius-lg: 12px;

  // ============================================
  // END CUSTOM BRANDING
  // ============================================
}
```

**Files modified**:
- [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss)

### Step 4.2: Document Customizations

**File**: Create `CUSTOMIZATION_NOTES.md` in repository root

```markdown
# Brand Customization Notes

This document tracks all branding customizations made to this fork of the Stellar Disbursement Platform Frontend.

## Customized Files

### Fonts
- `src/styles/fonts.scss` - Custom font declarations
- `src/styles/styles.scss` - Font variable overrides
- `public/fonts/` - Custom font files (if applicable)
- `index.html` - Google Fonts imports (if applicable)

### Logos
- `public/favicon.ico` - Browser favicon
- `public/icon.svg` - Scalable app icon
- `public/apple-touch-icon.png` - iOS icon
- `public/icon-192.png` - PWA icon (small)
- `public/icon-512.png` - PWA icon (large)
- `src/assets/app-logo.svg` - Main application logo
- `src/components/Logo.tsx` - Logo component
- `public/manifest.json` - PWA metadata

### Colors
- `src/styles/styles.scss` - Color variable overrides

### Metadata
- `index.html` - Title, description, theme color
- `public/manifest.json` - App name, description, theme

## Brand Assets

### Fonts
- Family: [Your Font Name]
- Weights: 400, 500, 600, 700
- Source: [Google Fonts / Custom]

### Colors
- Primary: #______
- Success: #______
- Error: #______
- Warning: #______
- Info: #______

### Logos
- Format: SVG (primary), PNG (fallbacks)
- Color mode: [Full color / Monochrome / Adaptive]

## Forward Compatibility Strategy

All customizations use CSS custom property overrides, allowing the underlying Stellar Design System to be updated without conflicts. Custom files are clearly marked and documented.

### Merging Upstream Changes

When updating from upstream:
```bash
git remote add upstream https://github.com/stellar/stellar-disbursement-platform-frontend.git
git fetch upstream
git merge upstream/main
# Resolve conflicts, prioritizing our branding customizations
```

### Files Safe to Overwrite
- Any files not listed in "Customized Files" above

### Files to Review Before Overwriting
- All files listed in "Customized Files" above
- Carefully merge changes while preserving branding

## Last Updated
[Date] - Initial branding implementation
```

**Files created**:
- `CUSTOMIZATION_NOTES.md` (new file in repository root)

---

## Phase 5: Forward Compatibility Setup

### Step 5.1: Create Override Pattern

To ensure forward compatibility with Stellar Design System updates, create a dedicated override file:

**File**: Create `src/styles/brand-overrides.scss`

```scss
// ============================================
// BRAND OVERRIDES
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
  --brand-font-base: 'YourBrandFont', 'Inter', sans-serif;
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
@use "./fonts.scss"; // Custom fonts
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
src/styles/fonts.scss merge=ours
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

### Step 6.2: Verify Nginx Configuration

**File**: [`nginx.conf`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/nginx.conf)

**Current configuration serves assets correctly**:
```nginx
gzip_static on;  # Serves pre-compressed assets
try_files $uri /index.html index.htm;  # SPA routing
```

**Optional Enhancement** - Add caching headers for better performance:

**Create**: `nginx-custom.conf` (optional)

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
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;

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
}
```

**Update Dockerfile to use custom nginx config** (if created):
```dockerfile
# In runtime stage
COPY nginx-custom.conf /etc/nginx/conf.d/default.conf
```

**Files optionally created**:
- `nginx-custom.conf` (optional performance enhancement)

**Files optionally modified**:
- [`Dockerfile`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/Dockerfile) (if using custom nginx config)

### Step 6.3: Configure Environment Variables for Branding

**File**: Create `.env.example` for documentation

```env
# Application Configuration
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_HORIZON_URL=https://horizon.stellar.org

# Branding (if using runtime configuration)
REACT_APP_SITE_NAME=Your Application Name
REACT_APP_COMPANY_NAME=Your Company
REACT_APP_PRIMARY_COLOR=#YOUR_COLOR

# Feature Flags
REACT_APP_ENABLE_SINGLE_TENANT_MODE=false
REACT_APP_USE_SSO=false

# Analytics (optional)
REACT_APP_GA_TRACKING_ID=
```

**Files created**:
- `.env.example`

---

## Phase 7: Build and Test

### Step 7.1: Test Local Development Build

```bash
# Install dependencies
yarn install

# Start development server
yarn dev

# Open browser to http://localhost:5173
# Verify:
# - Custom fonts are loading
# - Logos appear correctly
# - Colors match brand palette
# - PWA manifest is correct
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
# - Logos are in build root and build/assets/images/
# - Styles are compiled correctly
```

### Step 7.3: Build Docker Image

```bash
# Build Docker image
docker build -t sdp-frontend-custom:latest .

# Verify build completed successfully
docker images | grep sdp-frontend-custom
```

### Step 7.4: Test Docker Container

```bash
# Run container
docker run -d -p 8080:80 --name sdp-frontend-test sdp-frontend-custom:latest

# Test in browser
open http://localhost:8080

# Verify:
# - Application loads
# - Fonts render correctly
# - Logos display properly
# - All routes work (SPA routing)
# - PWA manifest accessible at /manifest.json
# - Favicon loads at /favicon.ico

# Check nginx logs
docker logs sdp-frontend-test

# Stop and remove test container
docker stop sdp-frontend-test
docker rm sdp-frontend-test
```

### Step 7.5: Validate Assets in Built Container

```bash
# Run container with shell access
docker run -it --rm sdp-frontend-custom:latest sh

# Inside container, verify assets exist:
ls -la /usr/share/nginx/html/
ls -la /usr/share/nginx/html/assets/
ls -la /usr/share/nginx/html/assets/fonts/  # If using custom fonts

# Verify key files:
# - index.html
# - favicon.ico
# - icon.svg, icon-192.png, icon-512.png
# - apple-touch-icon.png
# - manifest.json
# - assets/ directory with hashed files
```

---

## Phase 8: Deployment Integration

### Step 8.1: Tag and Push Docker Image

```bash
# Tag for your registry
docker tag sdp-frontend-custom:latest your-registry.com/sdp-frontend-custom:v1.0.0
docker tag sdp-frontend-custom:latest your-registry.com/sdp-frontend-custom:latest

# Push to registry
docker push your-registry.com/sdp-frontend-custom:v1.0.0
docker push your-registry.com/sdp-frontend-custom:latest
```

### Step 8.2: Update Docker Compose (If Applicable)

**File**: Update your deployment's `docker-compose.yml`

```yaml
version: '3.8'

services:
  frontend:
    image: your-registry.com/sdp-frontend-custom:latest
    ports:
      - "80:80"
    environment:
      # Environment variables if needed
      - REACT_APP_API_URL=${API_URL}
    restart: unless-stopped
    networks:
      - sdp-network

networks:
  sdp-network:
    driver: bridge
```

### Step 8.3: Deploy to Production

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
- [ ] Logos display at correct sizes
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

### Step 10.1: Update Repository README

Add a "Customization" section to README.md:

```markdown
## Customization

This fork includes custom branding (fonts, logos, colors). See [CUSTOMIZATION_NOTES.md](./CUSTOMIZATION_NOTES.md) for details.

### Customized Files
- `src/styles/fonts.scss` - Custom fonts
- `src/styles/brand-overrides.scss` - Color and theme overrides
- `public/` - Icons and favicons
- `src/assets/app-logo.svg` - Application logo
- `src/components/Logo.tsx` - Logo component

### Updating from Upstream
```bash
git remote add upstream https://github.com/stellar/stellar-disbursement-platform-frontend.git
git fetch upstream
git merge upstream/main
# Review conflicts in customized files
```
```

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

### Step 10.3: Version and Tag

```bash
# Commit all changes
git add .
git commit -m "feat: implement custom branding (fonts, logos, colors)"

# Create annotated tag
git tag -a v1.0.0-branded -m "Initial branded version with custom fonts, logos, and colors"

# Push commits and tags
git push origin feature/custom-branding
git push origin v1.0.0-branded
```

---

## Summary of Modified Files

### Created Files
- [ ] `src/styles/fonts.scss` - Font declarations
- [ ] `src/styles/brand-overrides.scss` - Centralized overrides
- [ ] `src/components/Logo.tsx` - Logo component
- [ ] `src/assets/app-logo.svg` - Application logo
- [ ] `public/fonts/` - Custom font files (if applicable)
- [ ] `CUSTOMIZATION_NOTES.md` - Customization documentation
- [ ] `MAINTENANCE.md` - Maintenance procedures
- [ ] `.env.example` - Environment variable template
- [ ] `.gitattributes` - Merge strategy for brand files
- [ ] `nginx-custom.conf` - Enhanced nginx config (optional)

### Modified Files
- [ ] [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss) - Import overrides, add custom CSS
- [ ] [`index.html`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/index.html) - Title, fonts, meta tags
- [ ] [`public/manifest.json`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/manifest.json) - App name, theme color
- [ ] [`public/favicon.ico`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/favicon.ico) - Custom favicon
- [ ] [`public/icon.svg`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/icon.svg) - Custom icon
- [ ] [`public/apple-touch-icon.png`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/apple-touch-icon.png) - iOS icon
- [ ] [`public/icon-192.png`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/icon-192.png) - PWA icon
- [ ] [`public/icon-512.png`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/icon-512.png) - PWA icon
- [ ] [`.github/dependabot.yml`](https://github.com/stellar/stellar-disbursement-platform-frontend/tree/main/.github) - Monitor dependencies
- [ ] `README.md` - Add customization section
- [ ] [`Dockerfile`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/Dockerfile) - Optional nginx config update

---

## Forward Compatibility Strategy

### Design Principles

1. **CSS Custom Property Overrides**: All styling changes use CSS variable overrides rather than modifying component styles directly
2. **Separate Override Files**: Brand customizations are isolated in dedicated files (`fonts.scss`, `brand-overrides.scss`)
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
docker build -t sdp-frontend-custom:test .
docker run -d -p 8080:80 sdp-frontend-custom:test
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

---

## Acceptance Criteria

- [ ] Custom fonts load correctly in all browsers
- [ ] Application logo displays in header/appropriate locations
- [ ] Favicon and PWA icons match brand
- [ ] Colors match brand palette throughout application
- [ ] PWA manifest reflects custom branding
- [ ] Docker image builds successfully
- [ ] Application runs correctly in Docker container
- [ ] All routes work (SPA routing intact)
- [ ] Performance scores remain high (Lighthouse >90)
- [ ] Accessibility maintained (WCAG 2.1 AA)
- [ ] Documentation complete (CUSTOMIZATION_NOTES.md, MAINTENANCE.md)
- [ ] Forward compatibility strategy implemented
- [ ] QA passed on all target browsers
- [ ] Deployed to production successfully

---

**Ticket Created By**: [Your Name]
**Date**: [Date]
**Target Completion**: [Date]
