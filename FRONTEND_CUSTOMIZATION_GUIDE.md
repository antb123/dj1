# Stellar Disbursement Platform Frontend - Customization Guide

## Overview

The Stellar Disbursement Platform Frontend is a **React + TypeScript** application built with **Vite** that uses the **@stellar/design-system (SDS)** for styling and components.

**Repository**: https://github.com/stellar/stellar-disbursement-platform-frontend

**Tech Stack**:
- React + TypeScript (92.4%)
- Vite (build tool)
- SCSS (7.1%) for styling
- Stellar Design System v3.1.4
- Yarn package manager

---

## 📁 Directory Structure

```
stellar-disbursement-platform-frontend/
├── public/                      # Static assets
│   ├── apple-touch-icon.png    # iOS icon
│   ├── favicon.ico             # Browser favicon
│   ├── icon-192.png            # PWA icon (192x192)
│   ├── icon-512.png            # PWA icon (512x512)
│   ├── icon.svg                # Scalable icon
│   ├── manifest.json           # PWA manifest
│   └── resources/              # Additional resources
├── src/
│   ├── assets/                 # Logo and image assets
│   │   ├── logo-euroc.png      # EuroC currency logo
│   │   ├── logo-usdc.png       # USDC currency logo
│   │   └── logo-xlm.png        # XLM/Stellar logo
│   ├── components/             # React components
│   ├── pages/                  # Page components
│   ├── styles/                 # Global styles
│   │   ├── styles.scss         # Main stylesheet
│   │   └── styles-utils.scss   # SCSS utilities/mixins
│   ├── App.tsx                 # Main app component
│   └── index.tsx               # Entry point
├── package.json
├── vite.config.ts
└── tsconfig.json
```

---

## 🎨 How to Modify Fonts

### Method 1: Override Design System Variables (Recommended)

The application uses Stellar Design System fonts configured via CSS custom properties.

**Current Font Variables**:
- `--sds-ff-base` - Base font family
- `--sds-ff-monospace` - Monospace font (for code)
- `--sds-fw-regular` - Regular weight
- `--sds-fw-medium` - Medium weight
- `--sds-fw-semi-bold` - Semi-bold weight

**Steps to Change Fonts**:

1. **Add custom fonts to your project**:

   **Option A: Using Google Fonts**

   Edit `src/index.html` and add to the `<head>`:
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
   ```

   **Option B: Using Local Font Files**

   a. Create directory `public/fonts/` and add your font files (.woff2, .woff, .ttf)

   b. Create `src/styles/fonts.scss`:
   ```scss
   @font-face {
     font-family: 'YourCustomFont';
     src: url('/fonts/YourCustomFont-Regular.woff2') format('woff2'),
          url('/fonts/YourCustomFont-Regular.woff') format('woff');
     font-weight: 400;
     font-style: normal;
     font-display: swap;
   }

   @font-face {
     font-family: 'YourCustomFont';
     src: url('/fonts/YourCustomFont-Bold.woff2') format('woff2'),
          url('/fonts/YourCustomFont-Bold.woff') format('woff');
     font-weight: 700;
     font-style: normal;
     font-display: swap;
   }
   ```

2. **Override design system variables**:

   Edit `src/styles/styles.scss` and add at the top (after imports):
   ```scss
   @use "./styles-utils.scss" as *;
   @use "./fonts.scss"; // If using local fonts

   :root {
     // Override base font
     --sds-ff-base: 'Inter', 'YourCustomFont', -apple-system, BlinkMacSystemFont,
                    'Segoe UI', 'Roboto', sans-serif;

     // Override monospace font (optional)
     --sds-ff-monospace: 'Fira Code', 'Courier New', monospace;
   }

   // Apply to body
   body {
     font-family: var(--sds-ff-base);
     font-size: pxToRem(14px); // Adjust base size if needed
   }
   ```

3. **Test your changes**:
   ```bash
   yarn install
   yarn dev
   ```

### Method 2: Component-Level Font Changes

For specific components, you can override fonts in component SCSS files or inline styles:

```scss
.my-custom-component {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 16px;
}
```

---

## 🖼️ How to Modify Logos

### 1. Application Icon/Favicon

**Files to Replace** (in `public/` directory):
- `favicon.ico` - 16x16 or 32x32 browser icon
- `icon.svg` - Scalable vector icon
- `apple-touch-icon.png` - 180x180 iOS icon
- `icon-192.png` - 192x192 PWA icon
- `icon-512.png` - 512x512 PWA icon

**Steps**:

1. **Prepare your logo** in multiple formats and sizes:
   - SVG (scalable)
   - PNG: 180x180, 192x192, 512x512
   - ICO: 32x32 (use online converter)

2. **Replace files** in `public/`:
   ```bash
   # Example using your logo files
   cp ~/my-brand/logo.svg public/icon.svg
   cp ~/my-brand/logo-180.png public/apple-touch-icon.png
   cp ~/my-brand/logo-192.png public/icon-192.png
   cp ~/my-brand/logo-512.png public/icon-512.png
   cp ~/my-brand/favicon.ico public/favicon.ico
   ```

3. **Update manifest.json** in `public/`:
   ```json
   {
     "short_name": "Your App Name",
     "name": "Your Full Application Name",
     "icons": [
       {
         "src": "icon-192.png",
         "type": "image/png",
         "sizes": "192x192"
       },
       {
         "src": "icon-512.png",
         "type": "image/png",
         "sizes": "512x512"
       }
     ],
     "start_url": ".",
     "display": "standalone",
     "theme_color": "#000000",
     "background_color": "#ffffff"
   }
   ```

4. **Update references in `src/index.html`** (if needed):
   ```html
   <link rel="icon" type="image/svg+xml" href="/icon.svg" />
   <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
   ```

### 2. Currency/Token Logos

**Current logos** in `src/assets/`:
- `logo-euroc.png` - EuroC
- `logo-usdc.png` - USDC
- `logo-xlm.png` - Stellar Lumens

**To add or replace**:

1. **Add logo files** to `src/assets/`:
   ```bash
   # Add new token logos
   cp ~/logos/logo-mytoken.png src/assets/
   ```

2. **Import in components** where used:
   ```typescript
   import logoMyToken from 'assets/logo-mytoken.png';

   // In component JSX
   <img src={logoMyToken} alt="My Token" width={24} height={24} />
   ```

3. **Update asset references** in existing code:
   ```bash
   # Search for logo usage
   grep -r "logo-usdc" src/

   # Update imports in found files
   ```

### 3. Application Logo/Branding

If you need to add a main application logo (header logo, login page logo):

1. **Add logo to assets**:
   ```bash
   cp ~/branding/app-logo.svg src/assets/
   ```

2. **Create a Logo component** (`src/components/Logo.tsx`):
   ```typescript
   import appLogo from 'assets/app-logo.svg';

   export const Logo = ({ width = 120, height = 40 }) => {
     return (
       <img
         src={appLogo}
         alt="Application Name"
         width={width}
         height={height}
         className="app-logo"
       />
     );
   };
   ```

3. **Use in header/navigation components**:
   ```typescript
   import { Logo } from 'components/Logo';

   // In your header component
   <header>
     <Logo />
     {/* Other header content */}
   </header>
   ```

---

## 🎨 Additional Branding Customization

### Colors

The design system uses CSS custom properties for colors. Override in `src/styles/styles.scss`:

```scss
:root {
  // Primary brand colors
  --sds-clr-primary: #your-brand-color;

  // Gray scale (--sds-clr-gray-01 through --sds-clr-gray-12)
  --sds-clr-gray-01: #fafafa;
  --sds-clr-gray-12: #1a1a1a;

  // Semantic colors
  --sds-clr-red-10: #dc2626;    // Error states
  --sds-clr-green-10: #16a34a;  // Success states
  --sds-clr-amber-10: #f59e0b;  // Warning states
}
```

### Spacing

```scss
:root {
  --sds-gap-xs: 4px;
  --sds-gap-sm: 8px;
  --sds-gap-md: 16px;
  --sds-gap-lg: 24px;
  --sds-gap-xl: 32px;
  --sds-gap-xxl: 48px;
}
```

### Typography Scale

```scss
:root {
  --font-size-base: 14px;
  --font-size-lg: 16px;
  --font-size-xl: 18px;
}
```

---

## 🚀 Development Workflow

### 1. Setup

```bash
# Clone the repository
git clone https://github.com/stellar/stellar-disbursement-platform-frontend.git
cd stellar-disbursement-platform-frontend

# Install dependencies
yarn install
```

### 2. Development

```bash
# Start development server
yarn dev

# The app will be available at http://localhost:3000
```

### 3. Building

```bash
# Build for production
yarn build

# Preview production build
yarn preview
```

### 4. Testing Changes

```bash
# Run linting
yarn lint

# Format code
yarn format

# Type checking
yarn type-check
```

---

## 📝 Configuration Files

### Environment Variables

Create `.env` file for configuration:

```env
# API Configuration
REACT_APP_API_URL=https://api.yourdomain.com

# Branding
REACT_APP_SITE_NAME=Your Application Name
REACT_APP_COMPANY_NAME=Your Company

# Feature flags
REACT_APP_ENABLE_FEATURE_X=true
```

Access in code:
```typescript
const apiUrl = import.meta.env.REACT_APP_API_URL;
```

### Vite Configuration

Edit `vite.config.ts` for build customization:

```typescript
export default defineConfig({
  // Custom alias for easier imports
  resolve: {
    alias: {
      '@': '/src',
      '@assets': '/src/assets',
      '@components': '/src/components',
    },
  },
  // Other config...
});
```

---

## 🔍 Finding Components That Need Logo Updates

```bash
# Search for logo usage
grep -r "logo" src/ --include="*.tsx" --include="*.ts"

# Search for asset imports
grep -r "from.*assets" src/ --include="*.tsx" --include="*.ts"

# Search for image tags
grep -r "<img" src/ --include="*.tsx"
```

---

## ⚠️ Important Notes

1. **Design System Override Limitations**: The Stellar Design System controls many styles. Major changes may require forking or heavily overriding the design system.

2. **Build Output**: After modifications, always test the production build:
   ```bash
   yarn build
   yarn preview
   ```

3. **Caching**: Browser caching may prevent logo/font updates from showing. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R) to see changes.

4. **Asset Optimization**: Optimize images before adding:
   ```bash
   # Using imagemagick
   convert logo.png -resize 512x512 -quality 85 logo-optimized.png

   # Or use online tools like TinyPNG, Squoosh
   ```

5. **Font Performance**:
   - Use WOFF2 format (best compression)
   - Subset fonts to include only needed characters
   - Use `font-display: swap` to prevent FOIT (Flash of Invisible Text)

6. **Accessibility**: Ensure logos have proper `alt` text and color contrast meets WCAG 2.1 AA standards (4.5:1 for normal text).

---

## 📚 Resources

- **Stellar Design System**: https://github.com/stellar/stellar-design-system
- **Vite Documentation**: https://vitejs.dev/
- **React Documentation**: https://react.dev/
- **Google Fonts**: https://fonts.google.com/
- **Font Squirrel** (web font generator): https://www.fontsquirrel.com/tools/webfont-generator
- **SVGOMG** (SVG optimizer): https://jakearchibald.github.io/svgomg/

---

## 🆘 Troubleshooting

### Fonts not loading
- Check browser console for CORS errors
- Verify font file paths are correct
- Ensure font files are in `public/` directory or properly imported
- Check `font-display` property

### Logo not showing
- Verify file path and import statement
- Check file extension (.png, .svg, .jpg)
- Ensure file is in `src/assets/` or `public/` directory
- Hard refresh browser (Ctrl+Shift+R)

### Build fails after changes
- Run `yarn install` to ensure dependencies are up to date
- Check TypeScript errors: `yarn type-check`
- Verify SCSS syntax: `yarn lint`
- Clear cache: `rm -rf node_modules/.vite`

---

## Example: Complete Font and Logo Customization

Here's a complete example of customizing both fonts and logos:

```bash
# 1. Add custom fonts
mkdir -p public/fonts
cp ~/branding/MyFont-*.woff2 public/fonts/

# 2. Add logos
cp ~/branding/app-logo.svg src/assets/
cp ~/branding/favicon.ico public/
cp ~/branding/icon-192.png public/
cp ~/branding/icon-512.png public/
```

**Create `src/styles/fonts.scss`**:
```scss
@font-face {
  font-family: 'MyBrandFont';
  src: url('/fonts/MyFont-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}

@font-face {
  font-family: 'MyBrandFont';
  src: url('/fonts/MyFont-Bold.woff2') format('woff2');
  font-weight: 700;
  font-display: swap;
}
```

**Update `src/styles/styles.scss`**:
```scss
@use "./styles-utils.scss" as *;
@use "./fonts.scss";

:root {
  --sds-ff-base: 'MyBrandFont', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --sds-clr-primary: #FF6B35; // Your brand color
}

body {
  font-family: var(--sds-ff-base);
}
```

**Create `src/components/Logo.tsx`**:
```typescript
import appLogo from 'assets/app-logo.svg';

interface LogoProps {
  width?: number;
  height?: number;
}

export const Logo = ({ width = 150, height = 50 }: LogoProps) => (
  <img
    src={appLogo}
    alt="My Application"
    width={width}
    height={height}
    style={{ maxWidth: '100%', height: 'auto' }}
  />
);
```

**Test changes**:
```bash
yarn dev
```

---

## Summary Checklist

- [ ] Fonts added to `public/fonts/` or linked from Google Fonts
- [ ] Font faces defined in `src/styles/fonts.scss`
- [ ] Design system variables overridden in `src/styles/styles.scss`
- [ ] Favicons replaced in `public/` directory
- [ ] `manifest.json` updated with app name and colors
- [ ] Asset logos added to `src/assets/`
- [ ] Logo component created and used in app
- [ ] Changes tested in development (`yarn dev`)
- [ ] Production build tested (`yarn build && yarn preview`)
- [ ] Browser hard refresh performed to clear cache

---

**Need Help?**
- Check the repository issues: https://github.com/stellar/stellar-disbursement-platform-frontend/issues
- Review Stellar Design System documentation
- Ask in Stellar developer community
