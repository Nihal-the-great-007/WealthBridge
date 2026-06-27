"""
Patch index.html with:
1. Remove housing & home loan affordability section (inputs + output card)
2. Add GitHub repo button centered in the topbar
3. Make control console background black/transparent
4. Glassmorphism effect on all parameter section cards
"""

HTML_PATH = r"c:\Users\sharv\Documents\MarshCase1\MarshCase1\templates\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Original size: {len(html):,} bytes")

# ─────────────────────────────────────────────────────────────────
# 1. REMOVE Housing Inputs Section from Control Console
# ─────────────────────────────────────────────────────────────────
# Find and remove the entire housing inputs section card
housing_input_start = html.find("            <!-- Section 4: Housing & Home Loan -->")
housing_input_end   = html.find("            <div style=\"display:flex; flex-direction:column; gap:8px; margin-top:14px;\">")

if housing_input_start != -1 and housing_input_end != -1:
    html = html[:housing_input_start] + html[housing_input_end:]
    print("Removed: Housing inputs section from control console")
else:
    print("WARNING: Could not find housing input section to remove")

# ─────────────────────────────────────────────────────────────────
# 2. REMOVE Housing Output Card from right panel (Tab 1)
# ─────────────────────────────────────────────────────────────────
housing_card_start = html.find("          <!-- Housing & Home Loan Affordability Card -->")
housing_card_end   = html.find("          <!-- P10/P50/P90 Chart -->")

if housing_card_start != -1 and housing_card_end != -1:
    html = html[:housing_card_start] + html[housing_card_end:]
    print("Removed: Housing output card from right panel")
else:
    print("WARNING: Could not find housing output card to remove")

# ─────────────────────────────────────────────────────────────────
# 3. REMOVE Housing slider parameters from getSliderParams()
# ─────────────────────────────────────────────────────────────────
old_housing_params = """        housing_house_price: g('sl-house-price'),
        housing_down_payment_pct: g('sl-down-payment-pct') / 100,
        housing_loan_rate: g('sl-loan-rate') / 100,
        housing_loan_tenure: g('sl-loan-tenure'),
        housing_safe_emi_pct: g('sl-safe-emi-pct') / 100,"""
new_housing_params = ""

if old_housing_params in html:
    html = html.replace(old_housing_params, new_housing_params)
    print("Removed: Housing params from getSliderParams()")
else:
    print("WARNING: Could not find housing params in getSliderParams()")

# ─────────────────────────────────────────────────────────────────
# 4. REMOVE Housing display code from updateMetrics()
# ─────────────────────────────────────────────────────────────────
old_housing_metrics = """      // Render Housing & Home Loan Affordability Card
      if (d.housing) {
        const h = d.housing;
        document.getElementById('h-monthly-emi').textContent = fmtINR(h.monthly_emi) + ' / mo';
        document.getElementById('h-loan-amount-sub').textContent = 'Loan: ' + fmtINR(h.loan_amount, true);
        document.getElementById('h-safe-emi').textContent = fmtINR(h.safe_emi_limit) + ' / mo';
        document.getElementById('h-max-house').textContent = fmtINR(h.max_affordable_house_price, true);
        
        const statusTag = document.getElementById('housing-status-tag');
        if (h.is_affordable) {
          statusTag.className = 'tag green';
          statusTag.textContent = '✅ Safe & Affordable';
        } else {
          statusTag.className = 'tag red';
          statusTag.textContent = '🚨 Exceeds Safe Limit';
        }
      }"""
new_housing_metrics = ""

if old_housing_metrics in html:
    html = html.replace(old_housing_metrics, new_housing_metrics)
    print("Removed: Housing metrics update code from updateMetrics()")
else:
    print("WARNING: Could not find housing metrics update code")

# ─────────────────────────────────────────────────────────────────
# 5. REMOVE Housing reset code from resetToBase()
# ─────────────────────────────────────────────────────────────────
old_housing_reset1 = """      setSl('sl-house-price', p.housing_house_price || 15000000);
      setSl('sl-down-payment-pct', (p.housing_down_payment_pct || 0.20) * 100);
      setSl('sl-loan-rate', (p.housing_loan_rate || 0.075) * 100);
      setSl('sl-loan-tenure', p.housing_loan_tenure || 20);
      setSl('sl-safe-emi-pct', (p.housing_safe_emi_pct || 0.35) * 100);"""
old_housing_reset2 = """      document.getElementById('val-house-price').textContent = fmtINR(p.housing_house_price || 15000000);
      document.getElementById('val-down-payment-pct').textContent = ((p.housing_down_payment_pct || 0.20) * 100).toFixed(1) + '%';
      document.getElementById('val-loan-rate').textContent = ((p.housing_loan_rate || 0.075) * 100).toFixed(2) + '%';
      document.getElementById('val-loan-tenure').textContent = (p.housing_loan_tenure || 20) + ' yrs';
      document.getElementById('val-safe-emi-pct').textContent = ((p.housing_safe_emi_pct || 0.35) * 100).toFixed(1) + '%';"""

for old, name in [(old_housing_reset1, "housing reset sliders"), (old_housing_reset2, "housing reset labels")]:
    if old in html:
        html = html.replace(old, "")
        print(f"Removed: {name} from resetToBase()")
    else:
        print(f"WARNING: Could not find {name} in resetToBase()")

# ─────────────────────────────────────────────────────────────────
# 6. REMOVE Housing CSV export section from exportData()
# ─────────────────────────────────────────────────────────────────
old_housing_csv = """      if (h && h.house_price) {
        csvContent += "2. HOUSING AFFORDABILITY METRICS\\\\r\\\\n";
        csvContent += "Metric,Value,Threshold & Status\\\\r\\\\n";
        csvContent += `Target House Price,${h.house_price} INR,-\\\\r\\\\n`;
        csvContent += `Required Down Payment (INR),${h.down_payment_val} INR,${(h.down_payment_pct * 100).toFixed(1)}% of price\\\\r\\\\n`;
        csvContent += `Home Loan Amount,${h.loan_amount} INR,-\\\\r\\\\n`;
        csvContent += `Monthly Loan EMI,${h.monthly_emi} INR/month,-\\\\r\\\\n`;
        csvContent += `Safe EMI Limit,${h.safe_emi_limit} INR/month,${(p.housing_safe_emi_pct * 100).toFixed(1)}% of net income\\\\r\\\\n`;
        csvContent += `Affordability Verdict,${h.is_affordable ? "SAFE / AFFORDABLE" : "HIGH RISK / EXCEEDS LIMIT"},-\\\\r\\\\n`;
        csvContent += `Max Affordable House Price,${h.max_affordable_house_price} INR,Based on safe EMI threshold\\\\r\\\\n\\\\r\\\\n`;
      }"""
if old_housing_csv in html:
    html = html.replace(old_housing_csv, "")
    print("Removed: Housing export CSV block")
else:
    print("WARNING: Could not find housing CSV export block")

# ─────────────────────────────────────────────────────────────────
# 7. ADD GITHUB BUTTON in topbar center
# ─────────────────────────────────────────────────────────────────
old_topbar_end = """    <div class="topbar-right">"""
new_topbar_center = """    <!-- Centered GitHub link -->
    <div class="topbar-center">
      <a href="https://github.com/Nihal-the-great-007/WealthBridge" target="_blank" rel="noopener noreferrer"
         class="github-btn" id="github-link-btn" title="View WealthBridge on GitHub">
        <svg class="github-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
        </svg>
        <span class="github-btn-text">GitHub Repo</span>
      </a>
    </div>

    <div class="topbar-right">"""

if old_topbar_end in html:
    html = html.replace(old_topbar_end, new_topbar_center, 1)
    print("Added: GitHub button in topbar center")
else:
    print("WARNING: Could not find topbar-right div")

# ─────────────────────────────────────────────────────────────────
# 8. INJECT CSS for GitHub button + topbar center + Glassmorphism
# ─────────────────────────────────────────────────────────────────
new_css = """
    /* ─── Topbar layout: three-zone flex ─── */
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .topbar-center {
      display: flex;
      align-items: center;
      justify-content: center;
      flex: 1;
    }

    /* ─── GitHub button ─── */
    .github-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 20px;
      border-radius: 30px;
      border: 1px solid var(--panel-border);
      background: rgba(255, 255, 255, 0.06);
      backdrop-filter: blur(8px);
      color: var(--text-primary);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.2px;
      transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    }
    body.light-mode .github-btn {
      background: rgba(0, 131, 176, 0.06);
      border-color: rgba(0, 131, 176, 0.20);
    }
    .github-btn:hover {
      background: var(--purple);
      color: #fff;
      border-color: var(--purple);
      box-shadow: 0 4px 18px var(--purple-glow);
      transform: translateY(-1px);
    }
    .github-icon {
      width: 16px;
      height: 16px;
      flex-shrink: 0;
    }

    /* ─── Control Console: transparent glass background ─── */
    .console-glass-panel {
      background: rgba(0, 0, 0, 0.35) !important;
      backdrop-filter: blur(20px) !important;
      -webkit-backdrop-filter: blur(20px) !important;
      border: 1px solid rgba(0, 180, 219, 0.15) !important;
    }
    body.light-mode .console-glass-panel {
      background: rgba(255, 255, 255, 0.20) !important;
      border-color: rgba(0, 131, 176, 0.18) !important;
    }

    /* ─── Glassmorphism Section Cards ─── */
    .console-section-card {
      background: rgba(255, 255, 255, 0.04) !important;
      border: 1px solid rgba(255, 255, 255, 0.10) !important;
      backdrop-filter: blur(14px) !important;
      -webkit-backdrop-filter: blur(14px) !important;
      border-radius: var(--radius-md) !important;
      box-shadow: 
        0 4px 24px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
      transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    body.light-mode .console-section-card {
      background: rgba(255, 255, 255, 0.55) !important;
      border: 1px solid rgba(0, 131, 176, 0.18) !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      box-shadow:
        0 4px 24px rgba(0, 131, 176, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.90) !important;
    }
    .console-section-card:hover {
      background: rgba(0, 180, 219, 0.06) !important;
      border-color: rgba(0, 180, 219, 0.35) !important;
      box-shadow:
        0 8px 32px rgba(0, 180, 219, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
      transform: translateY(-1px) !important;
    }
    body.light-mode .console-section-card:hover {
      background: rgba(0, 131, 176, 0.08) !important;
      border-color: rgba(0, 131, 176, 0.35) !important;
      box-shadow:
        0 8px 32px rgba(0, 131, 176, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 1) !important;
    }

    /* ─── Slider value badge: glassmorphism pill ─── */
    .slider-value {
      background: rgba(0, 180, 219, 0.12) !important;
      border: 1px solid rgba(0, 180, 219, 0.25) !important;
      color: var(--purple) !important;
      padding: 3px 10px !important;
      border-radius: 20px !important;
      font-size: 11.5px !important;
      font-weight: 700 !important;
      backdrop-filter: blur(4px) !important;
      letter-spacing: 0.2px;
    }
    body.light-mode .slider-value {
      background: rgba(0, 131, 176, 0.08) !important;
      border-color: rgba(0, 131, 176, 0.22) !important;
    }

    /* ─── Input field: glassmorphism ─── */
    .styled-input {
      background: rgba(0, 0, 0, 0.25) !important;
      border: 1px solid rgba(0, 180, 219, 0.20) !important;
      backdrop-filter: blur(8px) !important;
      color: var(--text-primary) !important;
    }
    body.light-mode .styled-input {
      background: rgba(255, 255, 255, 0.70) !important;
      border-color: rgba(0, 131, 176, 0.20) !important;
    }
    .styled-input:focus {
      background: rgba(0, 180, 219, 0.06) !important;
      border-color: var(--purple) !important;
    }

    /* ─── Section header: slightly glowing text ─── */
    .section-header {
      text-shadow: 0 0 12px var(--purple-glow) !important;
    }

    /* ─── Mobile: hide github text on small screens ─── */
    @media (max-width: 768px) {
      .github-btn-text { display: none; }
      .github-btn {
        padding: 8px 10px;
        border-radius: 50%;
        min-width: 36px;
        justify-content: center;
      }
      .topbar-center { flex: none; }
    }
"""

# Insert before the closing </style> tag
insert_marker = "    /* ═══════════════════════════════════════════════════════════════════\n       MOBILE BOTTOM NAV BAR"
if insert_marker in html:
    html = html.replace(insert_marker, new_css + "\n" + insert_marker)
    print("Injected: GitHub + glassmorphism + console glass CSS")
else:
    # Fall back to injecting before </style>
    html = html.replace("  </style>", new_css + "\n  </style>", 1)
    print("Injected: CSS (fallback before </style>)")

# ─────────────────────────────────────────────────────────────────
# 9. ADD console-glass-panel class to the control console panel div
# ─────────────────────────────────────────────────────────────────
old_console_div = """          <div class="panel" style="padding: 18px; display: flex; flex-direction: column; gap: 16px; background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(12px); border-color: var(--panel-border);">"""
new_console_div = """          <div class="panel console-glass-panel" style="padding: 18px; display: flex; flex-direction: column; gap: 16px;">"""

if old_console_div in html:
    html = html.replace(old_console_div, new_console_div)
    print("Updated: Control console panel with console-glass-panel class")
else:
    print("WARNING: Could not find control console div to update")

# ─────────────────────────────────────────────────────────────────
# WRITE PATCHED HTML
# ─────────────────────────────────────────────────────────────────
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nFinal size: {len(html):,} bytes")
print("Patch complete!")
