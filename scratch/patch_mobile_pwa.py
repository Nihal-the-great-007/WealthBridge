"""
Patch index.html with:
1. PWA <head> meta tags (manifest link, apple-touch-icon, theme-color, iOS capable)
2. Mobile-responsive CSS (full layout overhaul for max-width: 768px)
3. Mobile bottom navigation bar
4. Install App button / banner
5. Service Worker registration script
"""
import re

HTML_PATH = r"c:\Users\sharv\Documents\MarshCase1\MarshCase1\templates\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────────
# 1. INJECT PWA META TAGS into <head> after charset/viewport metas
# ─────────────────────────────────────────────────────────────────
pwa_head_tags = """  <!-- PWA Install Support -->
  <link rel="manifest" href="/manifest.json" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
  <meta name="apple-mobile-web-app-title" content="WealthBridge" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="theme-color" content="#0083B0" />
  <meta name="msapplication-TileColor" content="#0083B0" />
"""

# Inject right before the Google Fonts <link>
html = html.replace(
    '  <link rel="preconnect" href="https://fonts.googleapis.com" />',
    pwa_head_tags + '  <link rel="preconnect" href="https://fonts.googleapis.com" />'
)

# ─────────────────────────────────────────────────────────────────
# 2. MOBILE CSS — inject before </style>
# ─────────────────────────────────────────────────────────────────
mobile_css = """
    /* ═══════════════════════════════════════════════════════════════════
       MOBILE BOTTOM NAV BAR (hidden on desktop)
       ═══════════════════════════════════════════════════════════════════ */
    .mobile-nav {
      display: none;
    }

    /* ═══════════════════════════════════════════════════════════════════
       PWA INSTALL BANNER
       ═══════════════════════════════════════════════════════════════════ */
    #pwa-install-banner {
      display: none;
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 9999;
      background: linear-gradient(135deg, #0083B0, #00b4db);
      color: #ffffff;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      gap: 14px;
      box-shadow: 0 -4px 20px rgba(0, 131, 176, 0.35);
      transform: translateY(100%);
      transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1);
    }
    #pwa-install-banner.visible {
      transform: translateY(0);
    }
    .pwa-banner-icon {
      font-size: 28px;
      flex-shrink: 0;
    }
    .pwa-banner-text {
      flex: 1;
    }
    .pwa-banner-title {
      font-size: 14px;
      font-weight: 800;
      line-height: 1.2;
    }
    .pwa-banner-sub {
      font-size: 11px;
      opacity: 0.85;
      margin-top: 2px;
    }
    .pwa-install-btn {
      background: rgba(255, 255, 255, 0.25);
      border: 1.5px solid rgba(255, 255, 255, 0.70);
      color: #ffffff;
      padding: 8px 18px;
      border-radius: 30px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
      transition: background 0.2s;
    }
    .pwa-install-btn:hover {
      background: rgba(255, 255, 255, 0.40);
    }
    .pwa-dismiss-btn {
      background: transparent;
      border: none;
      color: rgba(255, 255, 255, 0.70);
      font-size: 18px;
      cursor: pointer;
      padding: 4px;
      flex-shrink: 0;
      line-height: 1;
    }

    /* ═══════════════════════════════════════════════════════════════════
       MOBILE RESPONSIVE OVERRIDES  (max-width: 768px)
       ═══════════════════════════════════════════════════════════════════ */
    @media (max-width: 768px) {
      /* Top bar: compact */
      .topbar {
        padding: 0 14px;
        height: 58px;
      }
      .brand-icon {
        width: 34px;
        height: 34px;
        font-size: 16px;
      }
      .brand-name {
        font-size: 15px;
      }
      .brand-sub {
        display: none;
      }
      .topbar-right .export-text,
      .topbar-right .theme-toggle-text {
        display: none;
      }
      .topbar-right {
        gap: 6px;
      }
      .action-btn {
        padding: 8px 10px;
        border-radius: 50%;
        min-width: 36px;
        justify-content: center;
      }

      /* Hide desktop tabs bar, show mobile nav instead */
      .tabs-bar {
        display: none !important;
      }
      .mobile-nav {
        display: flex;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 200;
        background: var(--panel);
        border-top: 1px solid var(--panel-border);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
        padding: 0 0 env(safe-area-inset-bottom, 0px);
      }
      .mob-tab-btn {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3px;
        padding: 10px 8px;
        border: none;
        background: transparent;
        color: var(--text-secondary);
        font-size: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        border-top: 2px solid transparent;
      }
      .mob-tab-btn.active {
        color: var(--purple);
        border-top-color: var(--purple);
        background: var(--panel-hover);
      }
      .mob-tab-icon {
        font-size: 20px;
        line-height: 1;
      }

      /* Add padding so content isn't hidden behind bottom nav */
      body {
        padding-bottom: 70px;
      }

      /* Main content: reduced padding */
      .main-content {
        padding: 14px 14px;
      }

      /* Tab 1 grid: stack vertically */
      .tab1-grid {
        grid-template-columns: 1fr;
        gap: 16px;
      }

      /* Control console: compact */
      .control-console .panel {
        padding: 14px;
      }
      .console-section-card {
        padding: 12px;
        gap: 10px;
      }

      /* Metrics row: 1 column on very small, 2 columns on medium */
      .metrics-row {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
      }
      .metric-value {
        font-size: 18px;
      }

      /* Success callout: stack */
      .success-callout {
        flex-direction: column;
        gap: 10px;
        padding: 14px 16px;
      }
      .callout-text {
        max-width: 100%;
      }
      .callout-big-num {
        font-size: 32px;
      }

      /* Housing card: stack to 1 col */
      .housing-card-grid {
        grid-template-columns: 1fr;
        gap: 12px;
      }

      /* Charts: full height for touch */
      .chart-wrap {
        height: 260px;
      }

      /* Tab 3 grid: stack */
      .tab3-top {
        grid-template-columns: 1fr;
        gap: 16px;
      }
      .donut-wrap {
        width: 170px;
        height: 170px;
      }

      /* Wealth metrics: 2 columns */
      .wealth-metrics {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
      }
      .income-card-corpus {
        font-size: 17px;
      }

      /* Data table: horizontal scroll */
      .data-table-wrap {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
      }
      .data-table {
        min-width: 640px;
        font-size: 11.5px;
      }
      .data-table td, .data-table th {
        padding: 8px 10px;
      }

      /* Startup screen: larger text on mobile */
      .startup-title {
        font-size: 36px;
      }
      .startup-motto {
        font-size: 13px;
      }
      .startup-logo {
        width: 70px;
        height: 70px;
        font-size: 32px;
      }

      /* Panel title: smaller */
      .panel-title {
        font-size: 14px;
      }

      /* Footer: smaller */
      .footer {
        padding: 16px 14px;
        font-size: 10.5px;
        padding-bottom: 80px;
      }
    }

    @media (max-width: 380px) {
      /* Extra small phones */
      .metrics-row {
        grid-template-columns: 1fr;
      }
      .wealth-metrics {
        grid-template-columns: 1fr;
      }
      .startup-title {
        font-size: 28px;
        letter-spacing: -1px;
      }
    }
"""

# Inject before the closing </style> tag
html = html.replace("  </style>", mobile_css + "  </style>", 1)

# ─────────────────────────────────────────────────────────────────
# 3. ADD MOBILE NAV BAR + PWA INSTALL BANNER to <body>
# ─────────────────────────────────────────────────────────────────
mobile_nav_html = """
  <!-- ══════════════════════════════════ MOBILE BOTTOM NAVIGATION ══ -->
  <nav class="mobile-nav" role="tablist" aria-label="Mobile navigation">
    <button class="mob-tab-btn active" id="mob-tab-btn-1" onclick="switchTab(1)">
      <span class="mob-tab-icon">🔮</span>
      <span>Calculator</span>
    </button>
    <button class="mob-tab-btn" id="mob-tab-btn-2" onclick="switchTab(2)">
      <span class="mob-tab-icon">📈</span>
      <span>Salary</span>
    </button>
    <button class="mob-tab-btn" id="mob-tab-btn-3" onclick="switchTab(3)">
      <span class="mob-tab-icon">🧱</span>
      <span>Wealth</span>
    </button>
  </nav>

  <!-- ══════════════════════════════════ PWA INSTALL BANNER ══════ -->
  <div id="pwa-install-banner" role="complementary" aria-label="Install WealthBridge App">
    <div class="pwa-banner-icon">💎</div>
    <div class="pwa-banner-text">
      <div class="pwa-banner-title">Install WealthBridge</div>
      <div class="pwa-banner-sub">Add to Home Screen for offline access</div>
    </div>
    <button class="pwa-install-btn" id="pwa-install-confirm" onclick="installPWA()">
      📲 Install
    </button>
    <button class="pwa-dismiss-btn" onclick="dismissInstallBanner()" aria-label="Dismiss">✕</button>
  </div>
"""

# Insert immediately before the closing </body>
html = html.replace("</body>", mobile_nav_html + "\n</body>", 1)

# ─────────────────────────────────────────────────────────────────
# 4. PATCH switchTab to also update mobile nav buttons
# ─────────────────────────────────────────────────────────────────
old_switchtab = """    function switchTab(n) {
      document.querySelectorAll('.tab-btn').forEach((b, i) => {
        b.classList.toggle('active', i === n - 1);
        b.setAttribute('aria-selected', i === n - 1);
      });
      document.querySelectorAll('.tab-panel').forEach((p, i) => {
        p.classList.toggle('active', i === n - 1);
      });

      setTimeout(() => {
        Object.values(_charts).forEach(c => { if (c) c.resize(); });
      }, 80);
    }"""

new_switchtab = """    function switchTab(n) {
      document.querySelectorAll('.tab-btn').forEach((b, i) => {
        b.classList.toggle('active', i === n - 1);
        b.setAttribute('aria-selected', i === n - 1);
      });
      // Also update mobile bottom nav buttons
      document.querySelectorAll('.mob-tab-btn').forEach((b, i) => {
        b.classList.toggle('active', i === n - 1);
      });
      document.querySelectorAll('.tab-panel').forEach((p, i) => {
        p.classList.toggle('active', i === n - 1);
      });
      setTimeout(() => {
        Object.values(_charts).forEach(c => { if (c) c.resize(); });
      }, 80);
    }"""

html = html.replace(old_switchtab, new_switchtab)

# ─────────────────────────────────────────────────────────────────
# 5. INJECT SERVICE WORKER REGISTRATION + PWA INSTALL LOGIC
# ─────────────────────────────────────────────────────────────────
pwa_js = """
    /* ═══════════════════════════════════════════════════════════════════════════
       PWA SERVICE WORKER REGISTRATION + INSTALL PROMPT
       ═══════════════════════════════════════════════════════════════════════════ */
    let _pwaInstallEvent = null;

    // Register service worker
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js', { scope: '/' })
          .then(reg => console.log('[PWA] Service Worker registered:', reg.scope))
          .catch(err => console.warn('[PWA] Service Worker registration failed:', err));
      });
    }

    // Capture the install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      _pwaInstallEvent = e;
      const banner = document.getElementById('pwa-install-banner');
      if (banner && !localStorage.getItem('pwa-dismissed')) {
        // Small delay so it doesn't flash immediately on load
        setTimeout(() => {
          banner.classList.add('visible');
        }, 4500);
      }
    });

    function installPWA() {
      if (!_pwaInstallEvent) return;
      _pwaInstallEvent.prompt();
      _pwaInstallEvent.userChoice.then(choice => {
        if (choice.outcome === 'accepted') {
          console.log('[PWA] User accepted install');
          document.getElementById('pwa-install-banner').classList.remove('visible');
        }
        _pwaInstallEvent = null;
      });
    }

    function dismissInstallBanner() {
      const banner = document.getElementById('pwa-install-banner');
      if (banner) banner.classList.remove('visible');
      localStorage.setItem('pwa-dismissed', '1');
    }

    // iOS Safari: no beforeinstallprompt — show manual instructions
    const isIOS = /iphone|ipad|ipod/.test(navigator.userAgent.toLowerCase());
    const isInStandaloneMode = window.navigator.standalone === true;
    if (isIOS && !isInStandaloneMode && !localStorage.getItem('pwa-dismissed')) {
      setTimeout(() => {
        const banner = document.getElementById('pwa-install-banner');
        const installBtn = document.getElementById('pwa-install-confirm');
        if (banner && installBtn) {
          installBtn.textContent = '📲 Tap Share → Add to Home';
          installBtn.onclick = () => {
            dismissInstallBanner();
            alert('To install WealthBridge:\\n1. Tap the Share button (box with arrow) in Safari\\n2. Select "Add to Home Screen"\\n3. Tap "Add" to confirm');
          };
          banner.querySelector('.pwa-banner-sub').textContent = 'Use Safari Share → Add to Home Screen';
          banner.classList.add('visible');
        }
      }, 5000);
    }
"""

# Inject PWA JS right before the closing </script> tag at the very end
last_script_close = html.rfind("  </script>")
if last_script_close != -1:
    html = html[:last_script_close] + pwa_js + "\n  </script>" + html[last_script_close + len("  </script>"):]

# ─────────────────────────────────────────────────────────────────
# 6. WRITE PATCHED HTML
# ─────────────────────────────────────────────────────────────────
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Patched index.html with mobile CSS, bottom nav, PWA install, and service worker!")
print(f"Final size: {len(html):,} bytes")
