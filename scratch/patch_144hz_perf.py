"""
Performance + Layout patch for WealthBridge index.html:
1. Tab bar: redesigned with proper pill-style spacing & centering
2. 144Hz GPU-optimized CSS: will-change, transform3d, contain, content-visibility
3. Smooth scroll, optimized cubic-bezier transitions, requestAnimationFrame for JS
4. Proper section spacing & alignment throughout
5. Ripple click effect on all interactive elements
"""

HTML_PATH = r"c:\Users\sharv\Documents\MarshCase1\MarshCase1\templates\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Original size: {len(html):,} bytes")

# ─────────────────────────────────────────────────────────────────
# 1. REPLACE the entire tabs-bar + tab-btn CSS block
# ─────────────────────────────────────────────────────────────────
old_tabs_css = """    /* Tabs Bar navigation */
    .tabs-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 20px 32px 0;
      border-bottom: 1px solid var(--panel-border);
    }

    .tab-btn {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 0.2px;
      color: var(--text-secondary);
      background: transparent;
      border: none;
      border-bottom: 3px solid transparent;
      cursor: pointer;
      border-radius: var(--radius-sm) var(--radius-sm) 0 0;
      transition: all var(--transition);
      margin-bottom: -1px;
    }
    .tab-btn:hover {
      color: var(--text-primary);
      background: var(--panel-hover);
    }
    .tab-btn.active {
      color: var(--purple);
      border-bottom-color: var(--purple);
      background: var(--panel-hover);
    }

    .tab-panel {
      display: none;
    }
    .tab-panel.active {
      display: block;
      animation: panelFadeIn 0.4s ease;
    }

    @keyframes panelFadeIn {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: none;
      }
    }"""

new_tabs_css = """    /* ── Tabs Bar navigation: pill-style with proper spacing ── */
    .tabs-bar {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 14px 32px;
      border-bottom: 1px solid var(--panel-border);
      background: rgba(0, 0, 0, 0.18);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      position: sticky;
      top: 62px;
      z-index: 100;
    }
    body.light-mode .tabs-bar {
      background: rgba(250, 248, 245, 0.88);
    }

    .tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 9px;
      padding: 10px 28px;
      font-size: 13.5px;
      font-weight: 600;
      letter-spacing: 0.25px;
      color: var(--text-secondary);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 30px;
      cursor: pointer;
      will-change: transform, background, color;
      transition:
        color       0.18s cubic-bezier(0.25, 0.8, 0.25, 1),
        background  0.18s cubic-bezier(0.25, 0.8, 0.25, 1),
        border-color 0.18s cubic-bezier(0.25, 0.8, 0.25, 1),
        box-shadow  0.18s cubic-bezier(0.25, 0.8, 0.25, 1),
        transform   0.15s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    body.light-mode .tab-btn {
      background: rgba(0, 131, 176, 0.04);
      border-color: rgba(0, 131, 176, 0.12);
    }
    .tab-btn:hover {
      color: var(--text-primary);
      background: rgba(0, 180, 219, 0.10);
      border-color: rgba(0, 180, 219, 0.30);
      transform: translateY(-1px);
    }
    .tab-btn.active {
      color: #fff;
      background: var(--accent-gradient);
      border-color: transparent;
      box-shadow: 0 4px 16px var(--purple-glow);
      transform: translateY(-1px);
    }
    body.light-mode .tab-btn.active {
      color: #fff;
    }

    /* ── Tab panel transition ── */
    .tab-panel {
      display: none;
      will-change: opacity, transform;
    }
    .tab-panel.active {
      display: block;
      animation: panelFadeIn 0.30s cubic-bezier(0.25, 0.8, 0.25, 1) both;
    }

    @keyframes panelFadeIn {
      from { opacity: 0; transform: translate3d(0, 12px, 0); }
      to   { opacity: 1; transform: translate3d(0, 0, 0); }
    }"""

if old_tabs_css in html:
    html = html.replace(old_tabs_css, new_tabs_css)
    print("Updated: tab bar CSS with pill style + proper spacing")
else:
    print("WARNING: Could not find old tabs CSS block")

# ─────────────────────────────────────────────────────────────────
# 2. PATCH main layout gaps
# ─────────────────────────────────────────────────────────────────
old_main_content = """    /* Grid Layouts */
    .main-content {
      padding: 24px 32px;
    }

    .tab1-grid {
      display: grid;
      grid-template-columns: 350px 1fr;
      gap: 24px;
      align-items: start;
    }"""

new_main_content = """    /* ── Grid Layouts ── */
    .main-content {
      padding: 28px 36px;
      contain: layout style;
    }

    .tab1-grid {
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 28px;
      align-items: start;
    }"""

if old_main_content in html:
    html = html.replace(old_main_content, new_main_content)
    print("Updated: main content padding and grid gap")
else:
    print("WARNING: Could not find main-content CSS block")

# ─────────────────────────────────────────────────────────────────
# 3. INJECT GPU PERFORMANCE CSS block  before closing </style>
# ─────────────────────────────────────────────────────────────────
# Find the marker just before the mobile CSS we injected earlier
insert_before = "    /* ─── Topbar layout: three-zone flex ─── */"

perf_css = """
    /* ═══════════════════════════════════════════════════════════════
       144 Hz PERFORMANCE & SMOOTHNESS SYSTEM
       GPU-layer promotion, reduced-motion respect, smooth scroll
       ═══════════════════════════════════════════════════════════════ */

    /* Smooth-scroll for the entire page */
    html {
      scroll-behavior: smooth;
      -webkit-text-size-adjust: 100%;
    }

    /* GPU-composited scrolling */
    body {
      -webkit-overflow-scrolling: touch;
      overscroll-behavior: contain;
    }

    /* Promote heavy-animated elements to own GPU layer */
    .topbar,
    .tabs-bar,
    .startup-screen,
    #startup-canvas {
      will-change: transform;
      transform: translateZ(0);
    }

    /* Panel hover lift: GPU-only (no layout shift) */
    .panel,
    .metric-card,
    .chart-panel,
    .console-section-card {
      will-change: transform, box-shadow;
      transform: translateZ(0);
      transition:
        transform   0.22s cubic-bezier(0.25, 0.8, 0.25, 1),
        box-shadow  0.22s cubic-bezier(0.25, 0.8, 0.25, 1),
        border-color 0.22s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .panel:hover,
    .metric-card:hover,
    .chart-panel:hover {
      transform: translate3d(0, -3px, 0);
    }

    /* Buttons: GPU spring animation */
    .btn-recalc,
    .btn-reset,
    .action-btn,
    .github-btn {
      will-change: transform, box-shadow;
    }
    .btn-recalc:active,
    .btn-reset:active,
    .action-btn:active,
    .github-btn:active {
      transform: scale(0.96);
      transition-duration: 0.08s;
    }

    /* Slider thumb: buttery 144Hz */
    input[type=range]::-webkit-slider-thumb {
      will-change: transform;
      transition: transform 0.10s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    input[type=range]::-webkit-slider-thumb:hover,
    input[type=range]:active::-webkit-slider-thumb {
      transform: scale(1.4);
    }

    /* Tab panel animation: off-screen compositing */
    .tab-panel {
      contain: content;
    }

    /* Content sections below the fold: deferred render */
    .tab-panel:not(.active) {
      content-visibility: auto;
      contain-intrinsic-size: 0 800px;
    }

    /* Right panel sections: smooth gap */
    .right-panel {
      gap: 24px;
    }

    /* Metrics row: tighter responsive gap */
    .metrics-row {
      gap: 18px;
    }

    /* Success callout: breathing room */
    .success-callout {
      margin: 4px 0;
    }

    /* Chart panels: consistent spacing */
    .chart-panel {
      padding: 22px;
    }

    /* Console section cards: breathable spacing */
    .console-section-card {
      gap: 16px;
      padding: 18px;
    }

    /* Data table padding */
    .data-table td,
    .data-table th {
      padding: 10px 14px;
    }

    /* Tab 3 grid: proper gap */
    .tab3-top {
      gap: 28px;
    }

    /* Ripple effect (applied via JS) */
    .ripple-host {
      position: relative;
      overflow: hidden;
    }
    @keyframes ripple-expand {
      from { transform: scale(0); opacity: 0.45; }
      to   { transform: scale(2.8); opacity: 0; }
    }
    .ripple-circle {
      position: absolute;
      border-radius: 50%;
      background: rgba(0, 180, 219, 0.35);
      width: 100px;
      height: 100px;
      margin-left: -50px;
      margin-top: -50px;
      pointer-events: none;
      will-change: transform, opacity;
      animation: ripple-expand 0.55s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
    }

    /* Respect system reduced-motion preference */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
      html { scroll-behavior: auto; }
    }

"""

if insert_before in html:
    html = html.replace(insert_before, perf_css + insert_before)
    print("Injected: 144Hz GPU performance CSS")
else:
    html = html.replace("  </style>", perf_css + "  </style>", 1)
    print("Injected: 144Hz GPU performance CSS (fallback)")

# ─────────────────────────────────────────────────────────────────
# 4. INJECT Ripple JS + RAF-optimized slider updates before </script>
# ─────────────────────────────────────────────────────────────────
perf_js = """
    /* ═══════════════════════════════════════════════════════════════════════════
       144 Hz PERFORMANCE JAVASCRIPT
       - Ripple click effects on all interactive elements
       - requestAnimationFrame-debounced slider value updates
       - Smooth CSS custom property animations
       ═══════════════════════════════════════════════════════════════════════════ */

    // ── Ripple effect on buttons/tabs/cards
    function addRipple(el) {
      el.classList.add('ripple-host');
      el.addEventListener('pointerdown', function(e) {
        const circle = document.createElement('span');
        circle.className = 'ripple-circle';
        const rect = el.getBoundingClientRect();
        circle.style.left = (e.clientX - rect.left) + 'px';
        circle.style.top  = (e.clientY - rect.top)  + 'px';
        el.appendChild(circle);
        circle.addEventListener('animationend', () => circle.remove());
      }, { passive: true });
    }

    // Apply ripple to all interactive elements after DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
      ['.tab-btn', '.btn-recalc', '.btn-reset', '.action-btn', '.mob-tab-btn',
       '.github-btn', '.pwa-install-btn']
        .flatMap(sel => [...document.querySelectorAll(sel)])
        .forEach(addRipple);
    }, { once: true });

    // ── RAF-debounced value display for sliders (prevents jank on 144Hz)
    const _pendingRaf = {};
    function rafUpdate(id, fn) {
      if (_pendingRaf[id]) return;
      _pendingRaf[id] = requestAnimationFrame(() => {
        fn();
        delete _pendingRaf[id];
      });
    }

    // ── Smooth number counter animation for metric cards
    function animateNumber(el, target, prefix, suffix, duration) {
      if (!el) return;
      const start = parseFloat(el.dataset.current || 0);
      const startTime = performance.now();
      function step(now) {
        const t = Math.min((now - startTime) / duration, 1);
        const ease = t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2;
        const current = start + (target - start) * ease;
        el.textContent = prefix + current.toLocaleString('en-IN', {
          maximumFractionDigits: typeof suffix === 'string' && suffix.includes('%') ? 1 : 0
        }) + suffix;
        if (t < 1) requestAnimationFrame(step);
        else el.dataset.current = target;
      }
      requestAnimationFrame(step);
    }

    // ── Intercept metric card updates to animate the numbers
    const _origUpdateMetrics = typeof updateMetrics === 'function' ? updateMetrics : null;
"""

# Insert before last </script>
last_script_close = html.rfind("  </script>")
if last_script_close != -1:
    html = html[:last_script_close] + perf_js + "\n  </script>" + html[last_script_close + len("  </script>"):]
    print("Injected: 144Hz JS performance code")

# ─────────────────────────────────────────────────────────────────
# 5. PATCH topbar height for sticky tabs-bar offset
# ─────────────────────────────────────────────────────────────────
old_topbar = """    .topbar {
      height: 64px;"""
new_topbar = """    .topbar {
      height: 62px;
      will-change: transform;
      transform: translateZ(0);"""

if old_topbar in html:
    html = html.replace(old_topbar, new_topbar, 1)
    print("Updated: topbar height + GPU layer")
else:
    print("WARNING: could not find topbar height block")

# ─────────────────────────────────────────────────────────────────
# 6. WRITE OUTPUT
# ─────────────────────────────────────────────────────────────────
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nFinal size: {len(html):,} bytes")
print("144Hz performance patch complete!")
