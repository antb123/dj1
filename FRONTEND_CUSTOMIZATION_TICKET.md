# Frontend Customization Implementation Plan - FreedomPayWallet

## Overview
This ticket provides step-by-step instructions to customize colors, logos, and fonts for the Stellar Disbursement Platform Frontend with FreedomPayWallet branding, including integration with Banxa and Mercuryo payment on-ramp providers.

**Repository**: https://github.com/stellar/stellar-disbursement-platform-frontend

**Tech Stack**: React + TypeScript, Vite, SCSS, @stellar/design-system, Docker + Nginx

**Build Output**: `/build` directory → Docker image → Nginx

**Payment On-Ramps**: Banxa, Mercuryo

---

## Prerequisites

- [ ] Access to the frontend repository
- [ ] Node.js 22.x and Yarn installed locally
- [ ] Docker installed for building and testing
- [ ] Banxa API credentials (Sandbox and Production)
- [ ] Mercuryo API credentials (Sandbox and Production)
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
git checkout -b feature/fpw-branding-banxa-mercuryo

# Install dependencies
yarn install
```

---

## Phase 2: Payment On-Ramp Integration

### Step 2.1: Install Banxa SDK

**Banxa** is a compliant fiat-to-crypto payment gateway supporting 40+ countries.

```bash
# Install Banxa SDK
yarn add @banxa/web-sdk

# Or use CDN integration
```

**Create Banxa Service**: `src/services/banxa.service.ts`

```typescript
import { BanxaSDK } from '@banxa/web-sdk';

interface BanxaConfig {
  partnerId: string;
  apiKey: string;
  sandbox: boolean;
}

export class BanxaService {
  private sdk: BanxaSDK;

  constructor(config: BanxaConfig) {
    this.sdk = new BanxaSDK({
      partnerId: config.partnerId,
      apiKey: config.apiKey,
      isSandbox: config.sandbox,
    });
  }

  /**
   * Create a buy order for cryptocurrency
   */
  async createBuyOrder(params: {
    fiatAmount: number;
    fiatCurrency: string;
    cryptoCurrency: string;
    walletAddress: string;
    returnUrl: string;
  }) {
    try {
      const order = await this.sdk.createOrder({
        accountReference: params.walletAddress,
        fiatType: params.fiatCurrency,
        coinType: params.cryptoCurrency,
        fiatAmount: params.fiatAmount,
        walletAddress: params.walletAddress,
        returnUrl: params.returnUrl,
      });

      return order;
    } catch (error) {
      console.error('Banxa order creation failed:', error);
      throw error;
    }
  }

  /**
   * Get order status
   */
  async getOrderStatus(orderId: string) {
    try {
      return await this.sdk.getOrder(orderId);
    } catch (error) {
      console.error('Failed to fetch Banxa order:', error);
      throw error;
    }
  }

  /**
   * Get supported currencies
   */
  async getSupportedCurrencies() {
    try {
      return await this.sdk.getCurrencies();
    } catch (error) {
      console.error('Failed to fetch Banxa currencies:', error);
      throw error;
    }
  }

  /**
   * Calculate exchange rate
   */
  async getQuote(params: {
    fiatAmount: number;
    fiatCurrency: string;
    cryptoCurrency: string;
  }) {
    try {
      return await this.sdk.getQuote({
        source: params.fiatCurrency,
        target: params.cryptoCurrency,
        sourceAmount: params.fiatAmount,
      });
    } catch (error) {
      console.error('Failed to get Banxa quote:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const banxaService = new BanxaService({
  partnerId: import.meta.env.VITE_BANXA_PARTNER_ID || '',
  apiKey: import.meta.env.VITE_BANXA_API_KEY || '',
  sandbox: import.meta.env.VITE_BANXA_SANDBOX === 'true',
});
```

### Step 2.2: Install Mercuryo SDK

**Mercuryo** is a crypto on-ramp supporting 100+ countries with credit card, Apple Pay, Google Pay.

```bash
# Mercuryo uses widget-based integration (no npm package needed)
```

**Create Mercuryo Service**: `src/services/mercuryo.service.ts`

```typescript
interface MercuryoConfig {
  widgetId: string;
  secret: string;
  sandbox: boolean;
}

interface MercuryoWidgetParams {
  type: 'buy' | 'sell';
  currency: string;
  fiatCurrency: string;
  fiatAmount?: number;
  address: string;
  returnUrl?: string;
  merchantTransactionId?: string;
}

export class MercuryoService {
  private config: MercuryoConfig;
  private baseUrl: string;

  constructor(config: MercuryoConfig) {
    this.config = config;
    this.baseUrl = config.sandbox
      ? 'https://sandbox-exchange.mrcr.io'
      : 'https://exchange.mercuryo.io';
  }

  /**
   * Generate Mercuryo widget URL with signature
   */
  generateWidgetUrl(params: MercuryoWidgetParams): string {
    const queryParams = new URLSearchParams({
      widget_id: this.config.widgetId,
      type: params.type,
      currency: params.currency,
      fiat_currency: params.fiatCurrency,
      address: params.address,
      ...(params.fiatAmount && { fiat_amount: params.fiatAmount.toString() }),
      ...(params.returnUrl && { return_url: params.returnUrl }),
      ...(params.merchantTransactionId && {
        merchant_transaction_id: params.merchantTransactionId
      }),
    });

    // Add signature for security (server-side recommended)
    const signature = this.generateSignature(queryParams.toString());
    queryParams.append('signature', signature);

    return `${this.baseUrl}/?${queryParams.toString()}`;
  }

  /**
   * Open Mercuryo widget in iframe or popup
   */
  openWidget(params: MercuryoWidgetParams, mode: 'iframe' | 'popup' = 'iframe') {
    const url = this.generateWidgetUrl(params);

    if (mode === 'popup') {
      window.open(
        url,
        'MercuryoWidget',
        'width=420,height=720,location=no,menubar=no'
      );
    } else {
      // Return URL for iframe embedding
      return url;
    }
  }

  /**
   * Generate HMAC signature for request validation
   * NOTE: This should be done server-side for security
   */
  private generateSignature(data: string): string {
    // This is a simplified version - use server-side crypto library
    // For production, send request to backend to generate signature
    const crypto = require('crypto');
    return crypto
      .createHmac('sha256', this.config.secret)
      .update(data)
      .digest('hex');
  }

  /**
   * Get transaction status
   */
  async getTransactionStatus(merchantTransactionId: string) {
    try {
      const response = await fetch(
        `${this.baseUrl}/b2b/api/v1/merchants/transaction/${merchantTransactionId}`,
        {
          headers: {
            'Content-Type': 'application/json',
            'Mercuryo-Widget-Id': this.config.widgetId,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch transaction status');
      }

      return await response.json();
    } catch (error) {
      console.error('Mercuryo transaction status error:', error);
      throw error;
    }
  }

  /**
   * Get supported currencies
   */
  async getSupportedCurrencies() {
    try {
      const response = await fetch(`${this.baseUrl}/b2b/api/v1/currencies`, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch currencies');
      }

      return await response.json();
    } catch (error) {
      console.error('Mercuryo currencies error:', error);
      throw error;
    }
  }

  /**
   * Get exchange rate
   */
  async getRate(params: {
    from: string;
    to: string;
    amount: number;
  }) {
    try {
      const response = await fetch(
        `${this.baseUrl}/b2b/api/v1/rate?from=${params.from}&to=${params.to}&amount=${params.amount}`,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch rate');
      }

      return await response.json();
    } catch (error) {
      console.error('Mercuryo rate error:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const mercuryoService = new MercuryoService({
  widgetId: import.meta.env.VITE_MERCURYO_WIDGET_ID || '',
  secret: import.meta.env.VITE_MERCURYO_SECRET || '',
  sandbox: import.meta.env.VITE_MERCURYO_SANDBOX === 'true',
});
```

### Step 2.3: Create Payment Gateway Selection Component

**Create**: `src/components/PaymentGateway/PaymentGatewaySelector.tsx`

```typescript
import React, { useState } from 'react';
import { Button, Select } from '@stellar/design-system';
import { banxaService } from '@/services/banxa.service';
import { mercuryoService } from '@/services/mercuryo.service';

type PaymentProvider = 'banxa' | 'mercuryo';

interface PaymentGatewaySelectorProps {
  walletAddress: string;
  defaultCurrency?: string;
  onSuccess?: (provider: PaymentProvider, transactionId: string) => void;
  onError?: (error: Error) => void;
}

export const PaymentGatewaySelector: React.FC<PaymentGatewaySelectorProps> = ({
  walletAddress,
  defaultCurrency = 'USDC',
  onSuccess,
  onError,
}) => {
  const [provider, setProvider] = useState<PaymentProvider>('banxa');
  const [fiatAmount, setFiatAmount] = useState<number>(100);
  const [fiatCurrency, setFiatCurrency] = useState<string>('USD');
  const [loading, setLoading] = useState(false);

  const handleBanxaPurchase = async () => {
    setLoading(true);
    try {
      const order = await banxaService.createBuyOrder({
        fiatAmount,
        fiatCurrency,
        cryptoCurrency: defaultCurrency,
        walletAddress,
        returnUrl: window.location.origin + '/payment-callback',
      });

      // Redirect to Banxa checkout
      window.location.href = order.checkout_url;

      onSuccess?.('banxa', order.order_id);
    } catch (error) {
      console.error('Banxa purchase failed:', error);
      onError?.(error as Error);
    } finally {
      setLoading(false);
    }
  };

  const handleMercuryoPurchase = () => {
    setLoading(true);
    try {
      const widgetUrl = mercuryoService.generateWidgetUrl({
        type: 'buy',
        currency: defaultCurrency,
        fiatCurrency,
        fiatAmount,
        address: walletAddress,
        returnUrl: window.location.origin + '/payment-callback',
        merchantTransactionId: `fpw-${Date.now()}`,
      });

      // Open in popup or redirect
      window.open(widgetUrl, '_blank', 'width=420,height=720');

      onSuccess?.('mercuryo', `fpw-${Date.now()}`);
    } catch (error) {
      console.error('Mercuryo purchase failed:', error);
      onError?.(error as Error);
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = () => {
    if (provider === 'banxa') {
      handleBanxaPurchase();
    } else {
      handleMercuryoPurchase();
    }
  };

  return (
    <div className="payment-gateway-selector">
      <h3>Buy Cryptocurrency</h3>

      <div className="form-group">
        <label>Payment Provider</label>
        <Select
          value={provider}
          onChange={(e) => setProvider(e.target.value as PaymentProvider)}
        >
          <option value="banxa">Banxa (40+ countries)</option>
          <option value="mercuryo">Mercuryo (100+ countries)</option>
        </Select>
      </div>

      <div className="form-group">
        <label>Amount ({fiatCurrency})</label>
        <input
          type="number"
          value={fiatAmount}
          onChange={(e) => setFiatAmount(Number(e.target.value))}
          min={10}
          max={10000}
        />
      </div>

      <div className="form-group">
        <label>Currency</label>
        <Select
          value={fiatCurrency}
          onChange={(e) => setFiatCurrency(e.target.value)}
        >
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="GBP">GBP</option>
          <option value="AUD">AUD</option>
        </Select>
      </div>

      <div className="wallet-address">
        <strong>Wallet:</strong> {walletAddress.substring(0, 10)}...
      </div>

      <Button
        onClick={handlePurchase}
        disabled={loading}
        fullWidth
      >
        {loading ? 'Processing...' : `Buy with ${provider === 'banxa' ? 'Banxa' : 'Mercuryo'}`}
      </Button>

      {provider === 'banxa' && (
        <p className="provider-info">
          <small>Banxa supports credit/debit cards, bank transfers, and local payment methods.</small>
        </p>
      )}

      {provider === 'mercuryo' && (
        <p className="provider-info">
          <small>Mercuryo supports credit cards, Apple Pay, Google Pay, and bank transfers.</small>
        </p>
      )}
    </div>
  );
};
```

### Step 2.4: Environment Variables for Payment Gateways

**File**: Update `.env.example`

```env
# Banxa Configuration
VITE_BANXA_PARTNER_ID=your_banxa_partner_id
VITE_BANXA_API_KEY=your_banxa_api_key
VITE_BANXA_SANDBOX=true

# Mercuryo Configuration
VITE_MERCURYO_WIDGET_ID=your_mercuryo_widget_id
VITE_MERCURYO_SECRET=your_mercuryo_secret
VITE_MERCURYO_SANDBOX=true

# Application
VITE_APP_NAME=FreedomPayWallet
VITE_API_URL=https://api.freedompaywallet.com
```

**Files modified**:
- `.env.example` (created if doesn't exist)

### Step 2.5: Payment Callback Handler

**Create**: `src/pages/PaymentCallback.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { banxaService } from '@/services/banxa.service';
import { mercuryoService } from '@/services/mercuryo.service';

export const PaymentCallback: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'processing' | 'success' | 'error'>('processing');
  const [message, setMessage] = useState('Processing your payment...');

  useEffect(() => {
    const handleCallback = async () => {
      const provider = searchParams.get('provider');
      const orderId = searchParams.get('order_id');
      const transactionId = searchParams.get('transaction_id');

      try {
        if (provider === 'banxa' && orderId) {
          const order = await banxaService.getOrderStatus(orderId);

          if (order.status === 'completed') {
            setStatus('success');
            setMessage('Payment successful! Your crypto will arrive shortly.');
          } else if (order.status === 'failed') {
            setStatus('error');
            setMessage('Payment failed. Please try again.');
          }
        } else if (provider === 'mercuryo' && transactionId) {
          const transaction = await mercuryoService.getTransactionStatus(transactionId);

          if (transaction.status === 'paid') {
            setStatus('success');
            setMessage('Payment successful! Your crypto will arrive shortly.');
          } else if (transaction.status === 'failed') {
            setStatus('error');
            setMessage('Payment failed. Please try again.');
          }
        }

        // Redirect to wallet after 3 seconds
        setTimeout(() => {
          navigate('/wallet');
        }, 3000);
      } catch (error) {
        console.error('Payment callback error:', error);
        setStatus('error');
        setMessage('Error processing payment callback.');
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  return (
    <div className="payment-callback">
      <div className={`status-icon ${status}`}>
        {status === 'processing' && '⏳'}
        {status === 'success' && '✅'}
        {status === 'error' && '❌'}
      </div>
      <h2>{message}</h2>
      <p>Redirecting to wallet...</p>
    </div>
  );
};
```

---

## Phase 3: Font Customization - FreedomPayWallet Fonts

### Step 3.1: Update index.html with Google Fonts

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

### Step 3.2: Override Design System Font Variables

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

## Phase 4: Logo Customization - FreedomPayWallet

### Step 4.1: Update PWA Manifest with FreedomPayWallet Branding

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
  "description": "FreedomPayWallet - Your gateway to secure cryptocurrency transactions with Banxa and Mercuryo integration"
}
```

**Files modified**:
- [`public/manifest.json`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/manifest.json)

### Step 4.2: Create Logo Component with FreedomPayWallet Logo

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

## Phase 5: Color and Theme Customization

### Step 5.1: Override Design System Color Variables

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

## Phase 6: Docker Build Configuration

### Step 6.1: Verify Dockerfile Handles Assets

**File**: [`Dockerfile`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/Dockerfile)

**Current multi-stage build already handles**:
- Copies all source files
- Runs `yarn build` which processes assets via Vite
- Copies `/app/build/` to nginx

**No changes needed** to Dockerfile for basic asset handling.

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

---

## Phase 7: Build and Test

### Step 7.1: Test Local Development Build

```bash
# Install dependencies
yarn install

# Set up environment variables
cp .env.example .env
# Edit .env with your Banxa and Mercuryo credentials

# Start development server
yarn dev

# Open browser to http://localhost:5173
# Verify:
# ✓ FreedomPayWallet logo loads
# ✓ Inter and Plus Jakarta Sans fonts render
# ✓ Colors match brand palette
# ✓ Banxa integration works
# ✓ Mercuryo integration works
```

### Step 7.2: Test Payment Gateway Integration

```bash
# Test Banxa (sandbox)
# 1. Navigate to buy crypto page
# 2. Select Banxa provider
# 3. Enter amount and click "Buy"
# 4. Verify redirect to Banxa sandbox checkout
# 5. Complete test transaction
# 6. Verify callback handling

# Test Mercuryo (sandbox)
# 1. Navigate to buy crypto page
# 2. Select Mercuryo provider
# 3. Enter amount and click "Buy"
# 4. Verify Mercuryo widget opens
# 5. Complete test transaction
# 6. Verify callback handling
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
docker run -d -p 8080:80 \
  -e VITE_BANXA_PARTNER_ID=your_id \
  -e VITE_MERCURYO_WIDGET_ID=your_widget_id \
  --name fpw-frontend-test \
  fpw-frontend:latest

# Test in browser
open http://localhost:8080

# Verify:
# ✓ Application loads with FreedomPayWallet branding
# ✓ Fonts render correctly (Inter, Plus Jakarta Sans)
# ✓ Logo displays properly
# ✓ Payment gateways functional
# ✓ All routes work

# Stop and remove
docker stop fpw-frontend-test
docker rm fpw-frontend-test
```

---

## Phase 8: Deployment

### Step 8.1: Production Environment Variables

```env
# Production .env
VITE_BANXA_PARTNER_ID=production_partner_id
VITE_BANXA_API_KEY=production_api_key
VITE_BANXA_SANDBOX=false

VITE_MERCURYO_WIDGET_ID=production_widget_id
VITE_MERCURYO_SECRET=production_secret
VITE_MERCURYO_SANDBOX=false

VITE_APP_NAME=FreedomPayWallet
VITE_API_URL=https://api.freedompaywallet.com
VITE_HORIZON_URL=https://horizon.stellar.org
```

### Step 8.2: Deploy to Production

```bash
# Tag Docker image
docker tag fpw-frontend:latest your-registry.com/fpw-frontend:v1.0.0

# Push to registry
docker push your-registry.com/fpw-frontend:v1.0.0

# Deploy with docker-compose or kubernetes
docker-compose up -d frontend
```

---

## Summary of Modified Files

### Created Files
- [ ] `src/services/banxa.service.ts` - Banxa SDK integration
- [ ] `src/services/mercuryo.service.ts` - Mercuryo widget integration
- [ ] `src/components/PaymentGateway/PaymentGatewaySelector.tsx` - Payment UI
- [ ] `src/pages/PaymentCallback.tsx` - Payment callback handler
- [ ] `src/components/Logo.tsx` - FreedomPayWallet logo component
- [ ] `.env.example` - Environment configuration template
- [ ] `nginx-fpw.conf` - Enhanced nginx configuration (optional)
- [ ] `CUSTOMIZATION_NOTES.md` - Documentation
- [ ] `FRONTEND_CUSTOMIZATION_TICKET.md` - This document

### Modified Files
- [ ] [`index.html`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/index.html) - FPW fonts, logos, meta tags
- [ ] [`src/styles/styles.scss`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/src/styles/styles.scss) - Font and color overrides
- [ ] [`public/manifest.json`](https://github.com/stellar/stellar-disbursement-platform-frontend/blob/main/public/manifest.json) - App metadata
- [ ] `package.json` - Add @banxa/web-sdk dependency
- [ ] `src/App.tsx` - Add PaymentCallback route
- [ ] Navigation components - Add "Buy Crypto" link

---

## Integration Checklist

### Banxa Integration
- [ ] Obtain Banxa partner ID and API key
- [ ] Configure sandbox environment
- [ ] Test buy flow in sandbox
- [ ] Implement order status polling
- [ ] Handle webhooks (optional)
- [ ] Test production credentials
- [ ] Go live

### Mercuryo Integration
- [ ] Obtain Mercuryo widget ID
- [ ] Configure sandbox environment
- [ ] Test widget embedding
- [ ] Test buy flow in sandbox
- [ ] Implement transaction status checking
- [ ] Server-side signature generation
- [ ] Test production credentials
- [ ] Go live

### FreedomPayWallet Branding
- [ ] Logo displays correctly in header
- [ ] Favicons load on all devices
- [ ] Inter font loads and renders
- [ ] Plus Jakarta Sans loads for headings
- [ ] Colors match brand palette
- [ ] PWA manifest correct
- [ ] Mobile responsiveness verified

---

## Acceptance Criteria

- [ ] FreedomPayWallet logo displays in all sizes
- [ ] Inter (400, 600) and Plus Jakarta Sans (600) fonts load
- [ ] Banxa integration functional (sandbox and production)
- [ ] Mercuryo integration functional (sandbox and production)
- [ ] Payment callback handling works
- [ ] Transaction status tracking works
- [ ] Docker image builds successfully
- [ ] Application runs in Docker container
- [ ] All payment flows tested end-to-end
- [ ] Performance scores >90 (Lighthouse)
- [ ] Accessibility maintained (WCAG 2.1 AA)
- [ ] Cross-browser compatibility verified
- [ ] Production deployment successful

---

## Resources

### Banxa
- **Documentation**: https://docs.banxa.com/
- **SDK GitHub**: https://github.com/banxa/banxa-web-sdk
- **Sandbox**: https://checkout.banxa.com/sandbox
- **Support**: support@banxa.com

### Mercuryo
- **Documentation**: https://help.mercuryo.io/en/
- **Widget Guide**: https://help.mercuryo.io/en/articles/4519473-mercuryo-widget
- **Sandbox**: https://sandbox-exchange.mrcr.io
- **Support**: support@mercuryo.io

### FreedomPayWallet
- **Website**: https://freedompaywallet.com
- **Logo Assets**: See Step 1.1
- **Fonts**: Google Fonts (Inter, Plus Jakarta Sans)
- **CSS**: https://freedompaywallet.com/wp-content/uploads/elementor/css/post-9123.css

---

**Ticket Created By**: Claude
**Date**: 2025-11-14
**Target Completion**: [Set based on sprint planning]
