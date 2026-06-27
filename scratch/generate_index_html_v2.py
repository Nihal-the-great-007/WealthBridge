# Let's generate the updated templates/index.html v2
# Updates:
# - Accent color swapped from purple/violet to aqua blue in light mode and charts.
# - Default mode set to Bright Mode (light-mode body class by default).
# - Tiled background-pattern.jpg applied to light-mode background.
# - Startup screen background made bright, text made dark/high contrast.
# - Startup Guilloche canvas animation distributed vertically over the whole background in beige.

content = """<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>WealthBridge — Premium Retirement Planner</title>
  <meta name="description"
    content="High-fidelity interactive retirement corpus projection dashboard with Monte Carlo stochastic simulation — WealthBridge." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap"
    rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
  <script
    src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
  <style>
    /* 
       DESIGN SYSTEM - WealthBridge Sleek Cyber-Financial Dark Theme
     */
    :root {
      --bg: #0A0A0E;
      --panel: #12121A;
      --panel-border: rgba(0, 180, 219, 0.15);
      --panel-hover: rgba(0, 180, 219, 0.08);
      --purple: #00b4db; /* Aqua teal primary */
      --purple-dim: rgba(0, 180, 219, 0.12);
      --purple-glow: rgba(0, 180, 219, 0.30);
      --magenta: #E01E37; /* Contrast pink-red */
      --magenta-dim: rgba(224, 30, 55, 0.12);
      --magenta-glow: rgba(224, 30, 55, 0.35);
      --cyan: #00f2fe;
      --green: #00E676;
      --gold: #FFD700;
      --amber: #FF9100;
      --text-primary: #F5F5FA;
      --text-secondary: #A0A0BA;
      --text-muted: #5F5F75;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --transition: 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
      --font-mono: 'JetBrains Mono', monospace;
      --topbar-bg: rgba(10, 10, 14, 0.85);
      --input-bg: rgba(0, 0, 0, 0.4);
      --income-row-bg: rgba(0, 0, 0, 0.2);
      --table-thead-bg: rgba(18, 18, 26, 0.98);
      --accent-gradient: linear-gradient(135deg, #00b4db, #00f2fe);
    }

    /* Light Mode (Default Bright Mode) Overrides */
    body.light-mode {
      --bg: #FAF8F5; /* Warm off-white background */
      --panel: #FFFFFF;
      --panel-border: rgba(0, 131, 176, 0.15); /* Aqua blue border */
      --panel-hover: rgba(0, 131, 176, 0.06);
      --purple: #0083B0; /* Vibrant Aqua Blue */
      --purple-dim: rgba(0, 131, 176, 0.10);
      --purple-glow: rgba(0, 131, 176, 0.20);
      --magenta: #D81B60;
      --magenta-dim: rgba(216, 27, 96, 0.10);
      --magenta-glow: rgba(216, 27, 96, 0.20);
      --cyan: #0288D1;
      --green: #2E7D32;
      --gold: #F57C00;
      --amber: #EF6C00;
      --text-primary: #1E1E2F;
      --text-secondary: #5E5E70;
      --text-muted: #8E8E9F;
      --topbar-bg: rgba(250, 248, 245, 0.85);
      --input-bg: rgba(0, 0, 0, 0.03);
      --income-row-bg: rgba(0, 0, 0, 0.02);
      --table-thead-bg: rgba(250, 248, 245, 0.98);
      --accent-gradient: linear-gradient(135deg, #0083B0, #00b4db);
      
      /* Background pattern */
      background-image: url('/background-pattern.jpg');
      background-repeat: repeat;
      background-position: top left;
    }

    /* Reset & Base Rules */
    *,
    *::before,
    *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: 'Inter', system-ui, sans-serif;
      background-color: var(--bg);
      color: var(--text-primary);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.5;
      transition: background-color var(--transition), color var(--transition);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: var(--panel);
    }
    ::-webkit-scrollbar-thumb {
      background: var(--purple);
      border-radius: 4px;
    }

    /* Top Bar Header */
    .topbar {
      position: sticky;
      top: 0;
      z-index: 100;
      background: var(--topbar-bg);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--panel-border);
      padding: 0 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 70px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-icon {
      width: 42px;
      height: 42px;
      background: var(--accent-gradient);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      box-shadow: 0 4px 15px var(--purple-glow);
    }

    .brand-name {
      font-size: 20px;
      font-weight: 800;
      letter-spacing: -0.5px;
      background: var(--accent-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-sub {
      font-size: 11px;
      color: var(--text-secondary);
      font-weight: 500;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    /* Action Buttons styling */
    .action-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      background: var(--purple-dim);
      border: 1px solid var(--purple);
      border-radius: 30px;
      color: var(--purple);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all var(--transition);
    }
    .action-btn:hover {
      background: var(--purple);
      color: #fff;
      box-shadow: 0 0 15px var(--purple-glow);
    }

    .theme-toggle-btn {
      background: transparent;
      border: 1px solid var(--panel-border);
      color: var(--text-primary);
    }
    .theme-toggle-btn:hover {
      background: var(--panel-hover);
      color: var(--text-primary);
      box-shadow: none;
    }

    /* Startup/Splash Screen (Bright/Beige Concept) */
    #startup-screen {
      position: fixed;
      inset: 0;
      z-index: 10000;
      background: #FAF8F5; /* Warm off-white background */
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }

    #startup-canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      pointer-events: none;
    }

    .startup-content {
      position: relative;
      z-index: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 30px;
    }

    .startup-logo {
      width: 90px;
      height: 90px;
      background: var(--accent-gradient);
      border-radius: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 42px;
      box-shadow: 0 4px 20px rgba(0, 131, 176, 0.25);
      margin-bottom: 24px;
      animation: logoEntrance 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
      opacity: 0;
      transform: translateY(-20px);
    }

    @keyframes logoEntrance {
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .startup-title {
      font-size: 52px;
      font-weight: 900;
      letter-spacing: -2px;
      color: #1E1E2F;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #1E1E2F 40%, #0083B0 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      opacity: 0;
      transform: scale(0.95);
      animation: titleEntrance 1s ease-out 0.3s forwards;
    }

    @keyframes titleEntrance {
      to {
        opacity: 1;
        transform: scale(1);
      }
    }

    .startup-motto {
      font-size: 16px;
      font-weight: 600;
      color: rgba(30, 30, 47, 0.75);
      letter-spacing: 0.5px;
      margin-bottom: 40px;
      max-width: 480px;
      line-height: 1.4;
      opacity: 0;
      animation: mottoEntrance 1s ease-out 0.8s forwards;
    }

    @keyframes mottoEntrance {
      to {
        opacity: 1;
      }
    }

    .startup-progress-container {
      width: 280px;
      height: 5px;
      background: rgba(0, 0, 0, 0.06);
      border-radius: 3px;
      overflow: hidden;
      margin-bottom: 16px;
      opacity: 0;
      animation: fadeIn 0.5s ease-out 1.2s forwards;
    }

    .startup-progress-bar {
      width: 0%;
      height: 100%;
      background: var(--accent-gradient);
      border-radius: 3px;
      transition: width 0.3s ease;
    }

    .startup-status {
      font-size: 11px;
      color: rgba(30, 30, 47, 0.6);
      letter-spacing: 1px;
      text-transform: uppercase;
      opacity: 0;
      font-family: var(--font-mono);
      animation: fadeIn 0.5s ease-out 1.4s forwards;
    }

    @keyframes fadeIn {
      to {
        opacity: 1;
      }
    }

    /* Tabs Bar navigation */
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
    }

    /* Grid Layouts */
    .main-content {
      padding: 24px 32px;
    }

    .tab1-grid {
      display: grid;
      grid-template-columns: 350px 1fr;
      gap: 24px;
      align-items: start;
    }

    /* Control Console Card Structure */
    .control-console {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-lg);
      padding: 24px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
      transition: all var(--transition);
    }

    .console-section-card {
      background: rgba(0, 0, 0, 0.18);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: var(--radius-md);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: all var(--transition);
    }
    body.light-mode .console-section-card {
      background: rgba(255, 255, 255, 0.85);
      border-color: rgba(0, 131, 176, 0.08);
      box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .console-section-card:hover {
      border-color: rgba(0, 180, 219, 0.25);
      background: rgba(0, 180, 219, 0.02);
    }
    body.light-mode .console-section-card:hover {
      border-color: var(--purple);
      background: rgba(0, 131, 176, 0.02);
    }

    .section-header {
      font-size: 12px;
      font-weight: 800;
      color: var(--purple);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding-bottom: 6px;
      margin-bottom: 4px;
    }
    body.light-mode .section-header {
      border-bottom-color: rgba(0, 131, 176, 0.10);
    }

    .panel-title {
      font-size: 16px;
      font-weight: 700;
      letter-spacing: -0.2px;
      margin-bottom: 16px;
      color: var(--text-primary);
    }

    /* Sliders & Inputs UI */
    .slider-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
    }

    .slider-label {
      color: var(--text-secondary);
      font-weight: 500;
    }

    .slider-value {
      font-family: var(--font-mono);
      font-weight: 600;
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.05);
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;
    }
    body.light-mode .slider-value {
      background: rgba(0, 0, 0, 0.05);
    }

    /* Custom range input styling */
    input[type=range] {
      -webkit-appearance: none;
      background: transparent;
      width: 100%;
      height: 18px;
    }
    input[type=range]:focus {
      outline: none;
    }
    input[type=range]::-webkit-slider-runnable-track {
      width: 100%;
      height: 5px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      transition: background 0.3s;
    }
    body.light-mode input[type=range]::-webkit-slider-runnable-track {
      background: rgba(0, 0, 0, 0.08);
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      height: 15px;
      width: 15px;
      border-radius: 50%;
      background: var(--purple);
      cursor: pointer;
      margin-top: -5px;
      box-shadow: 0 0 8px var(--purple-glow);
      transition: transform 0.15s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    input[type=range]::-webkit-slider-thumb:hover {
      transform: scale(1.3);
    }

    .input-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .input-label {
      font-size: 13px;
      color: var(--text-secondary);
      font-weight: 500;
    }

    .styled-input {
      background: var(--input-bg);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-sm);
      color: var(--text-primary);
      padding: 8px 12px;
      font-size: 14px;
      font-family: var(--font-mono);
      font-weight: 600;
      transition: border-color var(--transition);
    }
    .styled-input:focus {
      outline: none;
      border-color: var(--purple);
      box-shadow: 0 0 10px var(--purple-glow);
    }

    /* Buttons */
    .btn-recalc {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      width: 100%;
      padding: 12px;
      background: var(--accent-gradient);
      border: none;
      border-radius: var(--radius-md);
      color: #fff;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      transition: all var(--transition);
      box-shadow: 0 4px 15px var(--purple-glow);
    }
    .btn-recalc:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px var(--purple-glow);
    }
    .btn-recalc:active {
      transform: translateY(0);
    }

    .btn-reset {
      width: 100%;
      padding: 10px;
      background: transparent;
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      color: var(--text-secondary);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all var(--transition);
    }
    .btn-reset:hover {
      background: var(--panel-hover);
      color: var(--text-primary);
    }

    /* Right Dashboard Panel layout */
    .right-panel {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    /* Metrics Cards */
    .metrics-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
    }

    .metric-card {
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      padding: 18px;
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
      position: relative;
      overflow: hidden;
    }
    body.light-mode .metric-card {
      background: rgba(255, 255, 255, 0.90);
    }
    .metric-card::after {
      content: '';
      position: absolute;
      top: 0; left: 0; width: 4px; height: 100%;
      background: var(--purple);
    }
    .metric-card.magenta::after {
      background: var(--magenta);
    }
    .metric-card.cyan::after {
      background: var(--cyan);
    }

    .metric-label {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
    }

    .metric-value {
      font-size: 26px;
      font-weight: 900;
      letter-spacing: -0.5px;
      margin-bottom: 4px;
      font-family: var(--font-mono);
    }
    .metric-value.purple { color: var(--purple); }
    .metric-value.cyan { color: var(--cyan); }
    .metric-value.magenta { color: var(--magenta); }

    .metric-sub {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* Success / Survival Callout */
    .success-callout {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: linear-gradient(135deg, rgba(0, 180, 219, 0.06), rgba(157, 78, 221, 0.06));
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      padding: 20px 24px;
      box-shadow: inset 0 0 20px rgba(0, 180, 219, 0.03);
    }
    body.light-mode .success-callout {
      background: linear-gradient(135deg, rgba(0, 131, 176, 0.04), rgba(0, 180, 219, 0.04));
      box-shadow: none;
    }

    .callout-text {
      max-width: 70%;
    }

    .callout-label {
      font-size: 14px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }

    .callout-desc {
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.4;
    }

    .tag {
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .tag.green { background: rgba(0, 230, 118, 0.15); color: var(--green); border: 1px solid var(--green); }
    .tag.amber { background: rgba(255, 145, 0, 0.15); color: var(--amber); border: 1px solid var(--amber); }
    .tag.red { background: rgba(224, 30, 55, 0.15); color: var(--magenta); border: 1px solid var(--magenta); }
    body.light-mode .tag.green { background: rgba(46, 125, 50, 0.08); }
    body.light-mode .tag.amber { background: rgba(239, 108, 0, 0.08); }
    body.light-mode .tag.red { background: rgba(216, 27, 96, 0.08); }

    .callout-big-num {
      font-size: 40px;
      font-weight: 900;
      color: var(--green);
      font-family: var(--font-mono);
      letter-spacing: -1px;
    }
    .pct-sign {
      font-size: 20px;
      font-weight: 700;
    }

    /* Housing Card Styling */
    .housing-card {
      background: var(--panel);
      border: 1px solid rgba(0, 180, 219, 0.25);
      border-radius: var(--radius-md);
      padding: 20px;
      position: relative;
    }
    body.light-mode .housing-card {
      background: rgba(255, 255, 255, 0.90);
      border-color: rgba(0, 131, 176, 0.25);
    }
    .housing-card-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 12px;
    }
    .housing-subcard {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .housing-val {
      font-size: 20px;
      font-weight: 800;
      font-family: var(--font-mono);
      color: var(--text-primary);
    }

    /* Chart Panels */
    .chart-panel {
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-lg);
      padding: 24px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    body.light-mode .chart-panel {
      background: rgba(255, 255, 255, 0.92);
    }

    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }

    .chart-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .chart-legend {
      display: flex;
      gap: 16px;
      font-size: 11px;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--text-secondary);
    }

    .legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .chart-wrap {
      position: relative;
      height: 350px;
      width: 100%;
    }

    /* Tab 2 layout - Salary Projections and Table */
    .tab2-grid {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    /* Data Tables styling */
    .data-table-wrap {
      overflow-x: auto;
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      background: var(--panel);
    }
    body.light-mode .data-table-wrap {
      background: rgba(255, 255, 255, 0.90);
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }

    .data-table th {
      background: var(--table-thead-bg);
      color: var(--text-primary);
      font-weight: 700;
      padding: 14px 16px;
      border-bottom: 2px solid var(--panel-border);
      letter-spacing: 0.3px;
    }

    .data-table td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: var(--text-secondary);
      font-family: var(--font-mono);
      font-size: 12.5px;
    }
    body.light-mode .data-table td {
      border-bottom-color: rgba(0, 0, 0, 0.05);
      color: var(--text-primary);
    }

    .data-table tr:hover {
      background: var(--panel-hover);
    }

    .age-col {
      font-weight: 600;
      color: var(--text-primary);
    }

    .ctc-col {
      color: var(--purple);
      font-weight: 600;
    }

    .takehome-col {
      color: var(--cyan);
      font-weight: 600;
    }

    .elss-col {
      color: var(--magenta);
    }

    .income-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 14px;
      background: var(--income-row-bg);
      border-radius: var(--radius-sm);
      font-size: 13px;
      border: 1px solid rgba(255, 255, 255, 0.02);
    }
    body.light-mode .income-row {
      border-color: rgba(0, 0, 0, 0.03);
    }

    .income-row-label {
      color: var(--text-secondary);
    }

    .income-row-val {
      font-weight: 700;
      font-family: var(--font-mono);
    }
    .income-row-val.purple { color: var(--purple); }
    .income-row-val.cyan { color: var(--cyan); }
    .income-row-val.magenta { color: var(--magenta); }

    /* Tab 3 layout - Wealth Accumulation */
    .tab3-top {
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 24px;
      margin-bottom: 24px;
      align-items: start;
    }

    .donut-panel {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    body.light-mode .donut-panel {
      background: rgba(255, 255, 255, 0.90);
    }

    .donut-wrap {
      position: relative;
      width: 200px;
      height: 200px;
      margin: 20px 0;
    }

    .donut-center {
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      pointer-events: none;
    }

    .donut-center-label {
      font-size: 10px;
      font-weight: 700;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }

    .donut-center-value {
      font-size: 20px;
      font-weight: 900;
      color: var(--text-primary);
      font-family: var(--font-mono);
      margin-top: 4px;
    }

    .donut-legend {
      display: flex;
      flex-direction: column;
      gap: 8px;
      width: 100%;
      margin-top: 10px;
    }

    .donut-legend-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      transition: background 0.2s;
    }
    .donut-legend-item:hover {
      background: var(--panel-hover);
    }

    .donut-legend-left {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .donut-legend-swatch {
      width: 10px;
      height: 10px;
      border-radius: 3px;
    }

    .donut-legend-name {
      color: var(--text-secondary);
    }

    .donut-legend-val {
      font-family: var(--font-mono);
      font-weight: 600;
      color: var(--text-primary);
    }

    /* Wealth Cards */
    .wealth-metrics {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }

    .income-card {
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      transition: all var(--transition);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }
    body.light-mode .income-card {
      background: rgba(255, 255, 255, 0.90);
    }
    .income-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
    }

    .income-card-icon {
      font-size: 22px;
      margin-bottom: 4px;
    }

    .income-card-name {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .income-card-corpus {
      font-size: 22px;
      font-weight: 900;
      font-family: var(--font-mono);
      color: var(--text-primary);
    }
    .income-card.epf .income-card-corpus { color: var(--cyan); }
    .income-card.nps .income-card-corpus { color: var(--purple); }
    .income-card.elss .income-card-corpus { color: var(--magenta); }
    .income-card.wecare .income-card-corpus { color: var(--amber); }

    .income-card-rate {
      font-size: 10px;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* Income summary block */
    .income-summary {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 16px;
    }

    .total-income-row {
      background: rgba(0, 230, 118, 0.08) !important;
      border: 1px solid rgba(0, 230, 118, 0.25) !important;
      padding: 14px 18px !important;
      margin-top: 10px;
    }
    body.light-mode .total-income-row {
      background: rgba(46, 125, 50, 0.08) !important;
      border-color: rgba(46, 125, 50, 0.20) !important;
    }
    .total-income-row .income-row-label {
      font-weight: 800;
      color: var(--text-primary);
      font-size: 14px;
    }
    .total-income-row .income-row-val {
      font-size: 20px;
      font-weight: 900;
      color: var(--green);
    }

    /* Footer styling */
    .footer {
      border-top: 1px solid var(--panel-border);
      padding: 24px 32px;
      text-align: center;
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.6;
    }

    /* Visual layout cleanups */
    .panel, .chart-panel, .metric-card {
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18), 0 2px 4px rgba(0, 0, 0, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
    body.light-mode .panel, body.light-mode .chart-panel, body.light-mode .metric-card {
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04), 0 2px 4px rgba(0, 0, 0, 0.02);
      border: 1px solid rgba(0, 131, 176, 0.12);
    }

    /* PRINT LAYOUT STYLES - Visual Export */
    @media print {
      body {
        background: #ffffff !important;
        color: #000000 !important;
        font-size: 11pt !important;
        background-image: none !important; /* disable pattern on print */
      }
      
      .topbar, 
      .tabs-bar, 
      .control-console, 
      .action-btn, 
      .btn-recalc, 
      .btn-reset, 
      #startup-screen {
        display: none !important;
      }

      .tab-panel {
        display: block !important;
        opacity: 1 !important;
      }

      .main-content {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
      }

      .tab1-grid, .tab3-top {
        display: block !important;
        width: 100% !important;
      }

      .right-panel, .panel, .chart-panel, .metric-card, .housing-card {
        width: 100% !important;
        background: transparent !important;
        border: 1px solid #c8cbd0 !important;
        box-shadow: none !important;
        margin-bottom: 25px !important;
        padding: 16px !important;
        page-break-inside: avoid !important;
      }

      /* Force display all panels during print */
      #tab-panel-1, #tab-panel-2, #tab-panel-3 {
        display: block !important;
      }

      .chart-wrap {
        height: 280px !important;
        page-break-inside: avoid !important;
      }

      .data-table-wrap {
        overflow: visible !important;
        border: 1px solid #c8cbd0 !important;
      }

      .data-table {
        border-collapse: collapse !important;
        width: 100% !important;
      }

      .data-table th, .data-table td {
        border: 1px solid #c8cbd0 !important;
        padding: 8px 10px !important;
        color: #000000 !important;
      }

      .metric-value {
        font-size: 22px !important;
        color: #000000 !important;
      }

      .donut-legend {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 8px !important;
      }

      .donut-legend-item {
        border: 1px solid #ccc !important;
      }

      .wealth-metrics {
        grid-template-columns: repeat(2, 1fr) !important;
        page-break-inside: avoid !important;
      }

      .income-card {
        border: 1px solid #c8cbd0 !important;
      }
    }
  </style>
</head>

<body class="light-mode">

  <!-- Startup / Splash Screen -->
  <div id="startup-screen">
    <canvas id="startup-canvas"></canvas>
    <div class="startup-content">
      <div class="startup-logo">
        <span class="startup-icon">💎</span>
      </div>
      <h1 class="startup-title">WealthBridge</h1>
      <p class="startup-motto">Bridging Today's Income with Tomorrow's Retirement</p>
      <div class="startup-progress-container">
        <div class="startup-progress-bar" id="startup-progress"></div>
      </div>
      <div class="startup-status" id="startup-status">Initializing WealthBridge Engine...</div>
    </div>
  </div>

  <!-- ═══════════════════════════════════════════════════════════════ TOP BAR -->
  <header class="topbar">
    <div class="brand">
      <div class="brand-icon">💎</div>
      <div style="display:flex; flex-direction:column; gap:2px;">
        <div class="brand-name" style="line-height:1.2; font-weight:800; font-size:18px;">WealthBridge</div>
        <div class="brand-sub" style="font-size:10px; color:var(--text-secondary); font-weight:500; letter-spacing:0.3px;">Bridging Today's Income with Tomorrow's Retirement</div>
      </div>
    </div>
    <div class="topbar-right">
      <button id="export-csv-btn" class="action-btn" onclick="exportData()" title="Download CSV Projections">
        <span class="export-icon">📥</span>
        <span class="export-text">Export CSV</span>
      </button>
      <button id="print-btn" class="action-btn" onclick="window.print()" title="Print Dashboard Report">
        <span class="export-icon">🖨️</span>
        <span class="export-text">Print PDF</span>
      </button>
      <button id="theme-toggle" class="action-btn theme-toggle-btn" onclick="toggleTheme()" aria-label="Toggle bright mode" title="Toggle bright mode">
        <span class="theme-toggle-icon">🌙</span>
        <span class="theme-toggle-text">Dark Mode</span>
      </button>
      <span id="status-text" style="display: none !important;">Initialising…</span>
    </div>
  </header>

  <!-- ═══════════════════════════════════════════════════════════ TAB BUTTONS -->
  <nav class="tabs-bar" role="tablist" aria-label="Dashboard tabs">
    <button class="tab-btn active" id="tab-btn-1" role="tab" aria-selected="true" aria-controls="tab-panel-1"
      onclick="switchTab(1)">
      <span class="tab-icon">🔮</span> Unified Financial Calculator
    </button>
    <button class="tab-btn" id="tab-btn-2" role="tab" aria-selected="false" aria-controls="tab-panel-2"
      onclick="switchTab(2)">
      <span class="tab-icon">📈</span> Salary Projections & Income
    </button>
    <button class="tab-btn" id="tab-btn-3" role="tab" aria-selected="false" aria-controls="tab-panel-3"
      onclick="switchTab(3)">
      <span class="tab-icon">🧱</span> Wealth Accumulation Layer
    </button>
  </nav>

  <!-- ═══════════════════════════════════════════════ TAB 1: UNIFIED FINANCIAL CALCULATOR -->
  <div class="tab-panel active" id="tab-panel-1" role="tabpanel">
    <div class="main-content">
      <div class="tab1-grid">

        <!-- LEFT: Control Console -->
        <aside class="control-console">
          <div class="panel" style="padding: 18px; display: flex; flex-direction: column; gap: 16px; background: rgba(255, 255, 255, 0.45); backdrop-filter: blur(12px); border-color: var(--panel-border);">
            <div class="panel-title" style="margin-bottom: 2px; font-size: 16px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Control Console</div>

            <!-- Section 1: Member Profile -->
            <div class="console-section-card">
              <div class="section-header">👤 Member Profile</div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Current Age</span>
                  <span class="slider-value" id="val-age">28 yrs</span>
                </div>
                <input type="range" id="sl-age" min="18" max="58" value="28" step="1"
                  oninput="sliderUpdate('age', this.value, 'yrs')" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Retirement Age</span>
                  <span class="slider-value" id="val-ret-age">60 yrs</span>
                </div>
                <input type="range" id="sl-ret-age" min="50" max="70" value="60" step="1"
                  oninput="sliderUpdate('ret-age', this.value, 'yrs')" />
              </div>

              <div class="input-group">
                <label class="input-label" for="inp-ctc">Starting Annual CTC (₹)</label>
                <input type="number" class="styled-input" id="inp-ctc" value="2000000" min="300000" max="100000000"
                  step="100000" oninput="scheduleRecalc()" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Life Expectancy</span>
                  <span class="slider-value" id="val-life">85 yrs</span>
                </div>
                <input type="range" id="sl-life" min="70" max="100" value="85" step="1"
                  oninput="sliderUpdate('life', this.value, 'yrs')" />
              </div>
            </div>

            <!-- Section 2: Market Parameters -->
            <div class="console-section-card">
              <div class="section-header">📊 Market Parameters</div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Salary Growth Rate</span>
                  <span class="slider-value" id="val-sg">8.0%</span>
                </div>
                <input type="range" id="sl-sg" min="2" max="20" value="8" step="0.5"
                  oninput="sliderUpdate('sg', this.value, '%', 1)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Inflation Rate (CPI)</span>
                  <span class="slider-value" id="val-inf">6.0%</span>
                </div>
                <input type="range" id="sl-inf" min="2" max="14" value="6" step="0.5"
                  oninput="sliderUpdate('inf', this.value, '%', 1)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">ELSS Net Return</span>
                  <span class="slider-value" id="val-elss-r">12.0%</span>
                </div>
                <input type="range" id="sl-elss-r" min="6" max="22" value="12" step="0.25"
                  oninput="sliderUpdate('elss-r', this.value, '%', 2)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">NPS Blended Return</span>
                  <span class="slider-value" id="val-nps-r">10.75%</span>
                </div>
                <input type="range" id="sl-nps-r" min="5" max="18" value="10.75" step="0.25"
                  oninput="sliderUpdate('nps-r', this.value, '%', 2)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">EPF Interest Rate</span>
                  <span class="slider-value" id="val-epf-r">8.15%</span>
                </div>
                <input type="range" id="sl-epf-r" min="6" max="10" value="8.15" step="0.05"
                  oninput="sliderUpdate('epf-r', this.value, '%', 2)" />
              </div>
            </div>

            <!-- Section 3: Contributions -->
            <div class="console-section-card">
              <div class="section-header">💰 Contributions</div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Monthly ELSS SIP (₹)</span>
                  <span class="slider-value" id="val-elss-sip">₹10,000</span>
                </div>
                <input type="range" id="sl-elss-sip" min="0" max="50000" value="10000" step="1000"
                  oninput="sliderUpdate('elss-sip', this.value, '', 0, true)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">NPS Employee % of Basic</span>
                  <span class="slider-value" id="val-nps-e">5.0%</span>
                </div>
                <input type="range" id="sl-nps-e" min="0" max="15" value="5" step="0.5"
                  oninput="sliderUpdate('nps-e', this.value, '%', 1)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">WeCare Employee % of Basic</span>
                  <span class="slider-value" id="val-wc-e">10.0%</span>
                </div>
                <input type="range" id="sl-wc-e" min="0" max="20" value="10" step="0.5"
                  oninput="sliderUpdate('wc-e', this.value, '%', 1)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Safe Withdrawal Rate</span>
                  <span class="slider-value" id="val-swr">4.0%</span>
                </div>
                <input type="range" id="sl-swr" min="2" max="7" value="4" step="0.1"
                  oninput="sliderUpdate('swr', this.value, '%', 1)" />
              </div>
            </div>

            <!-- Section 4: Housing & Home Loan -->
            <div class="console-section-card" id="housing-inputs-section">
              <div class="section-header">🔑 Housing & Home Loan</div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Target House Price</span>
                  <span class="slider-value" id="val-house-price">₹15,000,000</span>
                </div>
                <input type="range" id="sl-house-price" min="2000000" max="50000000" value="15000000" step="500000"
                  oninput="sliderUpdate('house-price', this.value, '', 0, true)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Down Payment %</span>
                  <span class="slider-value" id="val-down-payment-pct">20.0%</span>
                </div>
                <input type="range" id="sl-down-payment-pct" min="10" max="60" value="20" step="1"
                  oninput="sliderUpdate('down-payment-pct', this.value, '%', 1)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Home Loan Rate</span>
                  <span class="slider-value" id="val-loan-rate">7.50%</span>
                </div>
                <input type="range" id="sl-loan-rate" min="5" max="15" value="7.5" step="0.05"
                  oninput="sliderUpdate('loan-rate', this.value, '%', 2)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Loan Tenure</span>
                  <span class="slider-value" id="val-loan-tenure">20 yrs</span>
                </div>
                <input type="range" id="sl-loan-tenure" min="5" max="30" value="20" step="1"
                  oninput="sliderUpdate('loan-tenure', this.value, 'yrs', 0)" />
              </div>

              <div class="slider-group">
                <div class="slider-header">
                  <span class="slider-label">Safe EMI % of Net</span>
                  <span class="slider-value" id="val-safe-emi-pct">35.0%</span>
                </div>
                <input type="range" id="sl-safe-emi-pct" min="15" max="50" value="35" step="1"
                  oninput="sliderUpdate('safe-emi-pct', this.value, '%', 1)" />
              </div>
            </div>

            <div style="display:flex; flex-direction:column; gap:8px; margin-top:14px;">
              <button class="btn-recalc" id="btn-calc" onclick="recalculate()">
                <div class="calc-spinner" id="calc-spinner"></div>
                <span id="btn-calc-text">⚡ Run Actuarial Simulation</span>
              </button>
              <button class="btn-reset" onclick="resetToBase()">↺ Reset to Base Case</button>
            </div>
          </div>
        </aside>

        <!-- RIGHT: Charts + Metrics -->
        <div class="right-panel">

          <!-- Top Metrics Row -->
          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-label">Total Investable Corpus</div>
              <div class="metric-value purple" id="m-corpus">—</div>
              <div class="metric-sub">at Retirement Age 60</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Monthly Retirement Income</div>
              <div class="metric-value cyan" id="m-income">—</div>
              <div class="metric-sub">EPF + NPS + WeCare + ELSS SWR</div>
            </div>
            <div class="metric-card magenta">
              <div class="metric-label">Replacement Ratio</div>
              <div class="metric-value" id="m-rr">—</div>
              <div class="metric-sub" id="m-rr-sub">Target: 50%–70%</div>
            </div>
          </div>

          <!-- Success Probability Callout -->
          <div class="success-callout">
            <div class="callout-text">
              <div class="callout-label">
                <span class="callout-label-icon">🎯</span>
                Corpus Survival Probability
              </div>
              <div class="callout-desc">
                Likelihood that the total investable corpus (EPF + NPS + ELSS)
                survives to <span id="callout-age">age 85</span> without depletion,
                across <strong>2,000 Monte Carlo paths</strong> with stochastic market returns.
              </div>
              <div style="margin-top:8px; display:flex; gap:10px; align-items:center;">
                <div class="tag" id="prob-tag">—</div>
                <span style="font-size:11px; color:var(--text-muted);">
                  σ: ELSS±15% · NPS±10% · EPF±2%
                </span>
              </div>
            </div>
            <div class="callout-big-num" id="success-prob">
              —<span class="pct-sign">%</span>
            </div>
          </div>

          <!-- Housing & Home Loan Affordability Card -->
          <div class="housing-card panel" id="housing-output-panel" style="margin-top: 5px; margin-bottom: 5px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--panel-border); padding-bottom:10px; margin-bottom:12px;">
              <div style="display:flex; align-items:center; gap:8px; font-weight:700; color:var(--text-primary); font-size:14px;">
                🏠 Housing & Home Loan Affordability Analysis
              </div>
              <div id="housing-status-tag" class="tag">—</div>
            </div>
            <div class="housing-card-grid">
              <div class="housing-subcard">
                <div style="font-size:11px; color:var(--text-secondary); margin-bottom:2px;">Monthly Loan EMI</div>
                <div id="h-monthly-emi" class="housing-val" style="color: var(--purple);">—</div>
                <div style="font-size:10px; color:var(--text-muted);" id="h-loan-amount-sub">Loan: —</div>
              </div>
              <div class="housing-subcard">
                <div style="font-size:11px; color:var(--text-secondary); margin-bottom:2px;">Safe EMI Limit</div>
                <div id="h-safe-emi" class="housing-val" style="color: var(--text-secondary);">—</div>
                <div style="font-size:10px; color:var(--text-muted);">Based on Year 1 Net Takehome</div>
              </div>
              <div class="housing-subcard">
                <div style="font-size:11px; color:var(--text-secondary); margin-bottom:2px;">Max Affordable House Price</div>
                <div id="h-max-house" class="housing-val" style="color: var(--cyan);">—</div>
                <div style="font-size:10px; color:var(--text-muted);">At current down payment %</div>
              </div>
            </div>
          </div>

          <!-- P10/P50/P90 Chart -->
          <div class="chart-panel">
            <div class="chart-header">
              <div class="chart-title">
                📉 Monte Carlo Wealth Trajectories — P10 / P50 / P90 Market Bands
              </div>
              <div class="chart-legend">
                <div class="legend-item">
                  <div class="legend-dot" style="background:#0077B6;"></div> P10 Pessimistic
                </div>
                <div class="legend-item">
                  <div class="legend-dot" style="background:#00b4db;"></div> P50 Expected
                </div>
                <div class="legend-item">
                  <div class="legend-dot" style="background:#00f2fe;"></div> P90 Optimistic
                </div>
              </div>
            </div>
            <div class="chart-wrap">
              <canvas id="chart-mc" aria-label="Monte Carlo wealth trajectories"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ════════════════════════════════════════ TAB 2: SALARY PROJECTIONS -->
  <div class="tab-panel" id="tab-panel-2" role="tabpanel">
    <div class="main-content">
      <div class="tab2-grid">

        <!-- Bar Chart -->
        <div class="chart-panel">
          <div class="chart-header">
            <div class="chart-title">Annual CTC vs Net Take-Home vs ELSS SIP</div>
          </div>
          <div class="chart-wrap" style="height:420px;">
            <canvas id="chart-salary" aria-label="Salary projections bar chart"></canvas>
          </div>
        </div>

        <!-- Data Table -->
        <div class="panel" style="padding:0; overflow:hidden;">
          <div style="padding:16px 18px; border-bottom:1px solid var(--panel-border);">
            <div class="panel-title" style="margin-bottom:0;">Year-by-Year Projection — 32-Year Career Horizon</div>
          </div>
          <div class="data-table-wrap" style="border:none; border-radius:0;">
            <table class="data-table" id="salary-table">
              <thead>
                <tr>
                  <th>Yr / Age</th>
                  <th>Annual CTC</th>
                  <th>Monthly Basic</th>
                  <th>EPF / mo</th>
                  <th>NPS / mo</th>
                  <th>WeCare / mo</th>
                  <th>ELSS SIP</th>
                  <th>Tax / mo</th>
                  <th>Net Take-Home</th>
                </tr>
              </thead>
              <tbody id="salary-table-body">
                <!-- Populated by JS -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- Bottom: Additional income decomposition -->
      <div style="margin-top:20px;">
        <div class="panel">
          <div class="panel-title">Pre-Tax Income Decomposition (Year 1 vs Year 32)</div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px;">
            <div class="income-row">
              <span class="income-row-label">Year 1 Annual CTC</span>
              <span class="income-row-val purple" id="sum-y1-ctc">—</span>
            </div>
            <div class="income-row">
              <span class="income-row-label">Year 1 Net Take-Home / mo</span>
              <span class="income-row-val cyan" id="sum-y1-th">—</span>
            </div>
            <div class="income-row">
              <span class="income-row-label">Year 32 Annual CTC</span>
              <span class="income-row-val purple" id="sum-y32-ctc">—</span>
            </div>
            <div class="income-row">
              <span class="income-row-label">Year 32 Net Take-Home / mo</span>
              <span class="income-row-val cyan" id="sum-y32-th">—</span>
            </div>
            <div class="income-row">
              <span class="income-row-label">Effective Tax Rate</span>
              <span class="income-row-val" id="sum-tax-rate">20%</span>
            </div>
            <div class="income-row">
              <span class="income-row-label">Total Retirement Deductions (Yr 1)</span>
              <span class="income-row-val magenta" id="sum-deductions">—</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ════════════════════════════════════ TAB 3: WEALTH ACCUMULATION -->
  <div class="tab-panel" id="tab-panel-3" role="tabpanel">
    <div class="main-content">

      <div class="tab3-top">
        <!-- Left: Donut Chart -->
        <div class="panel donut-panel">
          <div class="panel-title">Portfolio Breakdown at Retirement</div>
          <div class="donut-wrap">
            <canvas id="chart-donut" aria-label="Portfolio donut chart"></canvas>
            <div class="donut-center">
              <span class="donut-center-label">Total Corpus</span>
              <span class="donut-center-value" id="donut-total">—</span>
            </div>
          </div>
          <div class="donut-legend" id="donut-legend">
            <!-- Populated by JS -->
          </div>
        </div>

        <!-- Right: Corpus Curves Chart -->
        <div class="chart-panel">
          <div class="chart-header">
            <div class="chart-title">📈 Corpus Accumulation by Asset — EPF · NPS · ELSS</div>
            <div class="chart-legend">
              <div class="legend-item">
                <div class="legend-dot" style="background:var(--cyan)"></div> EPF
              </div>
              <div class="legend-item">
                <div class="legend-dot" style="background:var(--purple)"></div> NPS
              </div>
              <div class="legend-item">
                <div class="legend-dot" style="background:var(--magenta)"></div> ELSS
              </div>
              <div class="legend-item">
                <div class="legend-dot" style="background:var(--amber)"></div> WeCare
              </div>
              <div class="legend-item">
                <div class="legend-dot" style="background:var(--gold)"></div> Total
              </div>
            </div>
          </div>
          <div class="chart-wrap" style="height:340px;">
            <canvas id="chart-corpus" aria-label="Corpus accumulation curves"></canvas>
          </div>
        </div>
      </div>

      <!-- Corpus cards per vehicle -->
      <div class="wealth-metrics" style="margin-bottom:20px;">
        <div class="income-card epf">
          <div class="income-card-icon">🏦</div>
          <div class="income-card-name">EPF Corpus</div>
          <div class="income-card-corpus" id="wc-epf">—</div>
          <div class="income-card-rate">8.15% p.a. · Sovereign EEE</div>
        </div>
        <div class="income-card nps">
          <div class="income-card-icon">📋</div>
          <div class="income-card-name">NPS Corpus</div>
          <div class="income-card-corpus" id="wc-nps">—</div>
          <div class="income-card-rate">~10.75% blended · 40% annuity</div>
        </div>
        <div class="income-card elss">
          <div class="income-card-icon">📊</div>
          <div class="income-card-name">ELSS Corpus</div>
          <div class="income-card-corpus" id="wc-elss">—</div>
          <div class="income-card-rate">~12% net · 4% SWR drawdown</div>
        </div>
        <div class="income-card wecare">
          <div class="income-card-icon">🛡️</div>
          <div class="income-card-name">WeCare Corpus</div>
          <div class="income-card-corpus" id="wc-wecare">—</div>
          <div class="income-card-rate">Employee Cumulative Contribution</div>
        </div>
      </div>

      <!-- Income Summary at Retirement -->
      <div class="panel">
        <div class="panel-title">Retirement Income Architecture — Monthly Cash Flows at Age 60</div>
        <div class="income-summary">
          <div class="income-row">
            <span class="income-row-label">🏦 EPF Monthly Annuity (5.5% p.a.)</span>
            <span class="income-row-val cyan" id="ri-epf">—</span>
          </div>
          <div class="income-row">
            <span class="income-row-label">📋 NPS Monthly Annuity (40% @ 5.5%)</span>
            <span class="income-row-val purple" id="ri-nps">—</span>
          </div>
          <div class="income-row">
            <span class="income-row-label">🏢 WeCare DB Pension (pre-commutation)</span>
            <span class="income-row-val" style="color:var(--amber);" id="ri-wecare">—</span>
          </div>
          <div class="income-row">
            <span class="income-row-label">📊 ELSS 4% Safe Withdrawal Rate / 12</span>
            <span class="income-row-val magenta" id="ri-elss">—</span>
          </div>
          <div class="income-row total-income-row">
            <span class="income-row-label">💎 Total Monthly Retirement Income</span>
            <span class="income-row-val green" id="ri-total">—</span>
          </div>
          <div class="income-row total-income-row"
            style="background:rgba(157,78,221,0.08); border-color:rgba(157,78,221,0.25);">
            <span class="income-row-label" style="color:var(--text-primary); font-weight:700;">📐 Replacement Ratio
              (Income / Final Salary)</span>
            <span class="income-row-val" style="color:var(--purple); font-size:18px;" id="ri-rr">—</span>
          </div>
        </div>

        <!-- Lump Sums -->
        <div style="margin-top:16px; padding-top:16px; border-top:1px solid var(--panel-border);">
          <div class="section-header" style="margin-bottom:10px;">💼 Lump Sums Available at Retirement</div>
          <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:10px;">
            <div class="income-row">
              <span class="income-row-label">NPS Tax-Free Lump Sum (60%)</span>
              <span class="income-row-val purple" id="ls-nps">—</span>
            </div>
            <div class="income-row">
              <span class="income-row-label">WeCare Commuted Lump Sum (33%)</span>
              <span class="income-row-val" style="color:var(--amber);" id="ls-wc">—</span>
            </div>
            <div class="income-row">
              <span class="income-row-label">ELSS Available as Lump Sum</span>
              <span class="income-row-val magenta" id="ls-elss">—</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- ══════════════════════════════════════════════════════════════ FOOTER -->
  <footer class="footer">
    <div>
      <strong>WealthBridge Retirement Financial Planner</strong> — Track 1: Wealth & Pensions
    </div>
    <div style="margin-top:4px;">
      All projections are illustrative and based on stated assumptions. EPF: 8.15% · NPS: ~10.75% · ELSS: ~12%.
      Monte Carlo: 2,000 iterations · σ (ELSS 15%, NPS 10%, EPF 2%). Not financial advice.
    </div>
  </footer>

  <!-- ══════════════════════════════════════════════════════════ JAVASCRIPT -->
  <script>
    "use strict";
    /* ═══════════════════════════════════════════════════════════════════════════
       GLOBALS & STATE
       ═══════════════════════════════════════════════════════════════════════════ */
    let _data = null;   // Current active dataset
    let _baseData = null;   // Base-case snapshot for reset
    let _charts = {};     // Chart.js instances
    let _calcTimer = null;   // Debounce timer handle

    /* ═══════════════════════════════════════════════════════════════════════════
       INDIAN CURRENCY FORMATTER
       ═══════════════════════════════════════════════════════════════════════════ */
    function fmtINR(n, compact = false) {
      if (n === null || n === undefined || isNaN(n)) return '₹—';
      n = Math.round(n);
      if (compact) {
        if (Math.abs(n) >= 10_000_000) return '₹' + (n / 10_000_000).toFixed(2) + ' Cr';
        if (Math.abs(n) >= 100_000) return '₹' + (n / 100_000).toFixed(2) + ' L';
      }
      const sign = n < 0 ? '-' : '';
      let s = Math.abs(n).toString();
      let result = '';
      if (s.length > 3) {
        result = ',' + s.slice(-3);
        s = s.slice(0, -3);
        while (s.length > 2) {
          result = ',' + s.slice(-2) + result;
          s = s.slice(0, -2);
        }
        result = s + result;
      } else {
        result = s;
      }
      return sign + '₹' + result;
    }

    function fmtPct(v, decimals = 1) {
      if (v === null || v === undefined || isNaN(v)) return '—';
      return parseFloat(v).toFixed(decimals) + '%';
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       CHART.JS GLOBAL DEFAULTS
       ═══════════════════════════════════════════════════════════════════════════ */
    Chart.defaults.color = '#5E5E70';
    Chart.defaults.borderColor = 'rgba(0,131,176,0.12)';
    Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(255,255,255,0.95)';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(0,131,176,0.40)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.titleColor = '#1E1E2F';
    Chart.defaults.plugins.tooltip.bodyColor = '#5E5E70';
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    Chart.defaults.plugins.tooltip.callbacks = {
      label: ctx => {
        const v = ctx.parsed.y ?? ctx.parsed;
        return typeof v === 'number' ? '  ' + fmtINR(v, true) : '  ' + v;
      }
    };

    function updateChartThemeDefaults(isLight) {
      Chart.defaults.color = isLight ? '#5E5E70' : '#A0A0BA';
      Chart.defaults.borderColor = isLight ? 'rgba(0,131,176,0.12)' : 'rgba(0,180,219,0.12)';
      Chart.defaults.plugins.tooltip.backgroundColor = isLight ? 'rgba(255,255,255,0.95)' : 'rgba(22,22,31,0.95)';
      Chart.defaults.plugins.tooltip.borderColor = isLight ? 'rgba(0,131,176,0.40)' : 'rgba(0,180,219,0.40)';
      Chart.defaults.plugins.tooltip.titleColor = isLight ? '#1E1E2F' : '#F5F5FA';
      Chart.defaults.plugins.tooltip.bodyColor = isLight ? '#5E5E70' : '#A0A0BA';
    }

    function toggleTheme() {
      const isLight = document.body.classList.toggle('light-mode');
      localStorage.setItem('theme', isLight ? 'light' : 'dark');

      const btnIcon = document.querySelector('.theme-toggle-icon');
      const btnText = document.querySelector('.theme-toggle-text');
      if (btnIcon) btnIcon.textContent = isLight ? '🌙' : '☀️';
      if (btnText) btnText.textContent = isLight ? 'Dark Mode' : 'Bright Mode';

      updateChartThemeDefaults(isLight);

      const gridColorX = isLight ? 'rgba(0,131,176,0.06)' : 'rgba(0,180,219,0.06)';
      const gridColorY = isLight ? 'rgba(0,131,176,0.08)' : 'rgba(0,180,219,0.08)';
      const tickColor = isLight ? '#5E5E70' : '#A0A0BA';
      const labelColor = isLight ? '#5E5E70' : '#A0A0BA';

      if (_charts.mc) {
        _charts.mc.options.scales.x.grid.color = gridColorX;
        _charts.mc.options.scales.x.ticks.color = tickColor;
        _charts.mc.options.scales.y.grid.color = gridColorY;
        _charts.mc.options.scales.y.ticks.color = tickColor;
        _charts.mc.update();
      }
      if (_charts.salary) {
        _charts.salary.options.scales.x.ticks.color = tickColor;
        _charts.salary.options.scales.y.grid.color = gridColorX;
        _charts.salary.options.scales.y.ticks.color = tickColor;
        _charts.salary.options.plugins.legend.labels.color = labelColor;
        _charts.salary.update();
      }
      if (_charts.donut) {
        _charts.donut.data.datasets[0].borderColor = isLight ? '#FFFFFF' : '#12121A';
        _charts.donut.update();
      }
      if (_charts.corpus) {
        _charts.corpus.options.scales.x.grid.color = isLight ? 'rgba(0,131,176,0.05)' : 'rgba(0,180,219,0.05)';
        _charts.corpus.options.scales.x.ticks.color = tickColor;
        _charts.corpus.options.scales.y.grid.color = isLight ? 'rgba(0,131,176,0.07)' : 'rgba(0,180,219,0.07)';
        _charts.corpus.options.scales.y.ticks.color = tickColor;
        _charts.corpus.options.plugins.legend.labels.color = labelColor;
        _charts.corpus.update();
      }
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       CHART INITIALISATION HELPERS
       ═══════════════════════════════════════════════════════════════════════════ */
    function initMCChart(ages, p10, p50, p90) {
      const ctx = document.getElementById('chart-mc').getContext('2d');
      if (_charts.mc) _charts.mc.destroy();
      const isLight = document.body.classList.contains('light-mode');

      _charts.mc = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ages,
          datasets: [
            {
              label: 'P90 — Optimistic',
              data: p90,
              borderColor: '#00f2fe',
              borderWidth: 1.5,
              pointRadius: 0,
              tension: 0.4,
              fill: '+1',
              backgroundColor: () => {
                const g = ctx.createLinearGradient(0, 0, 0, 300);
                g.addColorStop(0, 'rgba(0,242,254,0.15)');
                g.addColorStop(1, 'rgba(0,242,254,0.01)');
                return g;
              },
            },
            {
              label: 'P50 — Expected Median',
              data: p50,
              borderColor: '#00b4db',
              borderWidth: 2.5,
              pointRadius: 0,
              tension: 0.4,
              fill: '+1',
              backgroundColor: () => {
                const g = ctx.createLinearGradient(0, 0, 0, 300);
                g.addColorStop(0, 'rgba(0,180,219,0.12)');
                g.addColorStop(1, 'rgba(0,180,219,0.01)');
                return g;
              },
            },
            {
              label: 'P10 — Pessimistic',
              data: p10,
              borderColor: '#0077B6',
              borderWidth: 1.5,
              borderDash: [5, 4],
              pointRadius: 0,
              tension: 0.4,
              fill: false,
            },
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                title: items => 'Age ' + items[0].label,
                label: item => '  ' + item.dataset.label + ': ' + fmtINR(item.parsed.y, true),
              }
            }
          },
          scales: {
            x: {
              grid: { color: isLight ? 'rgba(0,131,176,0.06)' : 'rgba(0,180,219,0.06)' },
              ticks: {
                color: isLight ? '#5E5E70' : '#606075', maxTicksLimit: 12,
                callback: v => 'Yr ' + (v + 1) + ' (Age ' + ages[v] + ')'
              }
            },
            y: {
              grid: { color: isLight ? 'rgba(0,131,176,0.08)' : 'rgba(0,180,219,0.08)' },
              ticks: {
                color: isLight ? '#5E5E70' : '#A0A0BA',
                callback: v => fmtINR(v, true),
              }
            }
          }
        }
      });
    }

    function initSalaryChart(salaryProj) {
      const ctx = document.getElementById('chart-salary').getContext('2d');
      if (_charts.salary) _charts.salary.destroy();
      const isLight = document.body.classList.contains('light-mode');

      const labels = salaryProj.map(r => 'Age ' + r.age);
      const ctcData = salaryProj.map(r => r.annual_ctc);
      const thData = salaryProj.map(r => r.net_takehome_pm * 12);
      const elssData = salaryProj.map(r => r.elss_sip_pm * 12);

      _charts.salary = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Annual CTC',
              data: ctcData,
              backgroundColor: 'rgba(0, 180, 219, 0.70)',
              borderColor: '#00b4db',
              borderWidth: 1,
              borderRadius: 3,
            },
            {
              label: 'Annual Net Take-Home',
              data: thData,
              backgroundColor: 'rgba(0, 242, 254, 0.55)',
              borderColor: '#00f2fe',
              borderWidth: 1,
              borderRadius: 3,
            },
            {
              label: 'Annual ELSS SIP',
              data: elssData,
              backgroundColor: 'rgba(224,30,55,0.55)',
              borderColor: '#E01E37',
              borderWidth: 1,
              borderRadius: 3,
            },
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: { boxWidth: 10, padding: 16, color: isLight ? '#5E5E70' : '#A0A0BA', font: { size: 11 } }
            },
            tooltip: {
              callbacks: {
                title: items => items[0].label,
                label: item => '  ' + item.dataset.label + ': ' + fmtINR(item.parsed.y, true),
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: isLight ? '#5E5E70' : '#606075', maxTicksLimit: 10, font: { size: 10 } }
            },
            y: {
              grid: { color: isLight ? 'rgba(0,131,176,0.06)' : 'rgba(0,180,219,0.06)' },
              ticks: { color: isLight ? '#5E5E70' : '#A0A0BA', callback: v => fmtINR(v, true) }
            }
          }
        }
      });
    }

    function initDonutChart(ret) {
      const ctx = document.getElementById('chart-donut').getContext('2d');
      if (_charts.donut) _charts.donut.destroy();
      const isLight = document.body.classList.contains('light-mode');

      const invested = ret.total_invested;
      const returns = ret.total_returns;
      const epfInv = ret.total_epf_invested;
      const npsInv = ret.total_nps_invested;
      const elssInv = ret.total_elss_invested;
      const wcInv = ret.wecare_cumul_emp || 0;

      _charts.donut = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['EPF Invested', 'NPS Invested', 'ELSS Invested', 'WeCare Invested', 'Compound Returns'],
          datasets: [{
            data: [epfInv, npsInv, elssInv, wcInv, returns],
            backgroundColor: [
              'rgba(0, 242, 254, 0.80)',
              'rgba(0, 180, 219, 0.80)',
              'rgba(224, 30, 55, 0.80)',
              'rgba(255, 145, 0, 0.80)',
              'rgba(255, 215, 0, 0.80)',
            ],
            borderColor: isLight ? '#FFFFFF' : '#12121A',
            borderWidth: 3,
            hoverOffset: 8,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '62%',
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: item => '  ' + item.label + ': ' + fmtINR(item.parsed, true),
              }
            }
          }
        }
      });

      const legendData = [
        { label: 'EPF Invested', val: epfInv, color: '#00f2fe' },
        { label: 'NPS Invested', val: npsInv, color: '#00b4db' },
        { label: 'ELSS Invested', val: elssInv, color: '#E01E37' },
        { label: 'WeCare Invested', val: wcInv, color: '#FF9100' },
        { label: 'Compound Returns', val: returns, color: '#FFD700' },
      ];

      document.getElementById('donut-legend').innerHTML = legendData.map(d => `
        <div class="donut-legend-item">
          <div class="donut-legend-left">
            <div class="donut-legend-swatch" style="background:${d.color};"></div>
            <span class="donut-legend-name">${d.label}</span>
          </div>
          <span class="donut-legend-val">${fmtINR(d.val, true)}</span>
        </div>
      `).join('');

      document.getElementById('donut-total').textContent = fmtINR(ret.total_corpus, true);
    }

    function initCorpusChart(corpusBuild) {
      const ctx = document.getElementById('chart-corpus').getContext('2d');
      if (_charts.corpus) _charts.corpus.destroy();
      const isLight = document.body.classList.contains('light-mode');

      const labels = corpusBuild.map(r => 'Age ' + r.age);

      const makeGrad = (hex) => () => {
        const g = ctx.createLinearGradient(0, 0, 0, 300);
        g.addColorStop(0, hex + '30');
        g.addColorStop(1, hex + '02');
        return g;
      };

      _charts.corpus = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'EPF',
              data: corpusBuild.map(r => r.epf_corpus),
              borderColor: '#00f2fe',
              backgroundColor: makeGrad('#00f2fe'),
              borderWidth: 2, pointRadius: 0, tension: 0.4, fill: true,
            },
            {
              label: 'NPS',
              data: corpusBuild.map(r => r.nps_corpus),
              borderColor: '#00b4db',
              backgroundColor: makeGrad('#00b4db'),
              borderWidth: 2, pointRadius: 0, tension: 0.4, fill: true,
            },
            {
              label: 'ELSS',
              data: corpusBuild.map(r => r.elss_corpus),
              borderColor: '#E01E37',
              backgroundColor: makeGrad('#E01E37'),
              borderWidth: 2.5, pointRadius: 0, tension: 0.4, fill: true,
            },
            {
              label: 'WeCare',
              data: corpusBuild.map(r => r.wecare_cumul),
              borderColor: '#FF9100',
              backgroundColor: makeGrad('#FF9100'),
              borderWidth: 2, pointRadius: 0, tension: 0.4, fill: true,
            },
            {
              label: 'Total',
              data: corpusBuild.map(r => r.total_corpus),
              borderColor: '#FFD700',
              backgroundColor: 'transparent',
              borderWidth: 3, pointRadius: 0, tension: 0.4, fill: false,
            },
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: {
              display: true, position: 'top',
              labels: { boxWidth: 10, padding: 16, color: isLight ? '#5E5E70' : '#A0A0BA', font: { size: 11 } }
            },
            tooltip: {
              callbacks: {
                title: items => items[0].label,
                label: item => '  ' + item.dataset.label + ': ' + fmtINR(item.parsed.y, true),
              }
            }
          },
          scales: {
            x: {
              grid: { color: isLight ? 'rgba(0,131,176,0.05)' : 'rgba(0,180,219,0.05)' },
              ticks: { color: isLight ? '#5E5E70' : '#606075', maxTicksLimit: 12, font: { size: 10 } }
            },
            y: {
              grid: { color: isLight ? 'rgba(0,131,176,0.07)' : 'rgba(0,180,219,0.07)' },
              ticks: { color: isLight ? '#5E5E70' : '#A0A0BA', callback: v => fmtINR(v, true) }
            }
          }
        }
      });
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       DOM UPDATE FUNCTIONS
       ═══════════════════════════════════════════════════════════════════════════ */
    function updateMetrics(d) {
      const ret = d.retirement;
      const mc = d.monte_carlo;

      document.getElementById('m-corpus').textContent = fmtINR(ret.total_corpus, true);
      document.getElementById('m-income').textContent = fmtINR(ret.total_monthly_income);
      
      const rr = parseFloat(ret.replacement_ratio);
      const rrEl = document.getElementById('m-rr');
      rrEl.textContent = fmtPct(rr);
      if (rr >= 70) { 
        rrEl.style.color = 'var(--green)'; 
        document.getElementById('m-rr-sub').textContent = '✅ Exceeds 70% target'; 
      } else if (rr >= 50) { 
        rrEl.style.color = 'var(--purple)'; 
        document.getElementById('m-rr-sub').textContent = '✅ On-Track (50%–70%)'; 
      } else { 
        rrEl.style.color = 'var(--magenta)'; 
        document.getElementById('m-rr-sub').textContent = '⚠️ Below 50% target'; 
      }

      const sp = mc.success_probability;
      document.getElementById('success-prob').innerHTML = sp.toFixed(1) + '<span class="pct-sign">%</span>';
      document.getElementById('callout-age').textContent = 'age ' + mc.life_expectancy;
      const tag = document.getElementById('prob-tag');
      if (sp >= 85) { tag.className = 'tag green'; tag.textContent = '✅ High Confidence'; }
      else if (sp >= 60) { tag.className = 'tag amber'; tag.textContent = '⚠️ Moderate Risk'; }
      else { tag.className = 'tag red'; tag.textContent = '🚨 High Depletion Risk'; }

      if (d.salary_proj && d.salary_proj.length > 0) {
        const y1 = d.salary_proj[0];
        const yn = d.salary_proj[d.salary_proj.length - 1];
        document.getElementById('sum-y1-ctc').textContent = fmtINR(y1.annual_ctc, true);
        document.getElementById('sum-y1-th').textContent = fmtINR(y1.net_takehome_pm);
        document.getElementById('sum-y32-ctc').textContent = fmtINR(yn.annual_ctc, true);
        document.getElementById('sum-y32-th').textContent = fmtINR(yn.net_takehome_pm);
        const deductions = y1.epf_emp_pm + y1.nps_emp_pm + y1.wecare_pm + y1.elss_sip_pm;
        document.getElementById('sum-deductions').textContent = fmtINR(deductions) + ' / mo';
        if (d.params && d.params.income_tax_rate !== undefined) {
          document.getElementById('sum-tax-rate').textContent = fmtPct(d.params.income_tax_rate * 100);
        }
      }

      document.getElementById('wc-epf').textContent = fmtINR(ret.epf_corpus, true);
      document.getElementById('wc-nps').textContent = fmtINR(ret.nps_corpus, true);
      document.getElementById('wc-elss').textContent = fmtINR(ret.elss_corpus, true);
      document.getElementById('wc-wecare').textContent = fmtINR(ret.wecare_corpus, true);

      document.getElementById('ri-epf').textContent = fmtINR(ret.epf_monthly_annuity) + ' / mo';
      document.getElementById('ri-nps').textContent = fmtINR(ret.nps_monthly_annuity) + ' / mo';
      document.getElementById('ri-wecare').textContent = fmtINR(ret.wecare_monthly_pre) + ' / mo';
      document.getElementById('ri-elss').textContent = fmtINR(ret.elss_monthly_swr) + ' / mo';
      document.getElementById('ri-total').textContent = fmtINR(ret.total_monthly_income) + ' / mo';
      document.getElementById('ri-rr').textContent = fmtPct(ret.replacement_ratio) + ' of Final Salary';

      document.getElementById('ls-nps').textContent = fmtINR(ret.nps_lumpsum, true);
      document.getElementById('ls-wc').textContent = fmtINR(ret.wecare_commuted_lumpsum, true);
      document.getElementById('ls-elss').textContent = fmtINR(ret.elss_corpus_full, true);

      // Render Housing & Home Loan Affordability Card
      if (d.housing) {
        const h = d.housing;
        document.getElementById('h-monthly-emi').textContent = fmtINR(h.monthly_emi) + ' / mo';
        document.getElementById('h-loan-amount-sub').textContent = 'Loan: ' + fmtINR(h.down_payment_pct * h.house_price || h.loan_amount, true);
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
      }
    }

    function buildSalaryTable(salaryProj) {
      const tbody = document.getElementById('salary-table-body');
      tbody.innerHTML = salaryProj.map(r => `
        <tr>
          <td class="age-col">Yr${r.year} / ${r.age}</td>
          <td class="ctc-col">${fmtINR(r.annual_ctc, true)}</td>
          <td>${fmtINR(r.basic_pm)}</td>
          <td>${fmtINR(r.epf_total_pm)}</td>
          <td>${fmtINR(r.nps_emp_pm + (r.nps_empr_pm || 0))}</td>
          <td>${fmtINR(r.wecare_pm)}</td>
          <td class="elss-col">${fmtINR(r.elss_sip_pm)}</td>
          <td>${fmtINR(r.income_tax_pm)}</td>
          <td class="takehome-col">${fmtINR(r.net_takehome_pm)}</td>
        </tr>
      `).join('');
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       RENDER ALL CHARTS + METRICS FROM DATA OBJECT
       ═══════════════════════════════════════════════════════════════════════════ */
    function renderAll(d) {
      _data = d;
      updateMetrics(d);
      buildSalaryTable(d.salary_proj);

      const mc = d.monte_carlo;
      initMCChart(mc.ages, mc.p10, mc.p50, mc.p90);
      initSalaryChart(d.salary_proj);
      initDonutChart(d.retirement);
      initCorpusChart(d.corpus_build);
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       API CALLS
       ═══════════════════════════════════════════════════════════════════════════ */
    const API_BASE = window.location.origin.startsWith('file') || !window.location.origin.includes('8000')
      ? 'http://127.0.0.1:8000'
      : '';

    async function fetchBaseData() {
      const res = await fetch(`${API_BASE}/api/data`);
      if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`);
      return res.json();
    }

    async function postCalculate(params) {
      const res = await fetch(`${API_BASE}/api/calculate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      });
      if (!res.ok) throw new Error(`Calculation error ${res.status}: ${await res.text()}`);
      return res.json();
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       SLIDER / INPUT EVENT HANDLERS
       ═══════════════════════════════════════════════════════════════════════════ */
    function sliderUpdate(id, rawVal, suffix, decimals = 0, isCurrency = false) {
      const v = parseFloat(rawVal);
      let display;
      if (isCurrency) {
        display = fmtINR(v);
      } else if (decimals > 0) {
        display = v.toFixed(decimals) + suffix;
      } else {
        display = v + ' ' + suffix;
      }
      document.getElementById('val-' + id).textContent = display;
      scheduleRecalc();
    }

    function scheduleRecalc() {
      clearTimeout(_calcTimer);
      _calcTimer = setTimeout(recalculate, 400);
    }

    function getSliderParams() {
      const g = id => parseFloat(document.getElementById(id).value);
      const age = g('sl-age');
      const retAge = g('sl-ret-age');
      const safeRetAge = Math.max(retAge, age + 1);

      return {
        current_age: age,
        retirement_age: safeRetAge,
        starting_ctc: parseFloat(document.getElementById('inp-ctc').value) || 2_000_000,
        salary_growth: g('sl-sg') / 100,
        inflation: g('sl-inf') / 100,
        elss_net_return: g('sl-elss-r') / 100,
        nps_blended_return: g('sl-nps-r') / 100,
        epf_return: g('sl-epf-r') / 100,
        elss_monthly_sip: g('sl-elss-sip'),
        nps_employee_pct: g('sl-nps-e') / 100,
        elss_swr: g('sl-swr') / 100,
        life_expectancy: g('sl-life'),
        wecare_employee_pct: g('sl-wc-e') / 100,
        wecare_pension_pct: 0.50,
        wecare_commutation_pct: 0.33,
        commutation_factor: 11.0,
        housing_house_price: g('sl-house-price'),
        housing_down_payment_pct: g('sl-down-payment-pct') / 100,
        housing_loan_rate: g('sl-loan-rate') / 100,
        housing_loan_tenure: g('sl-loan-tenure'),
        housing_safe_emi_pct: g('sl-safe-emi-pct') / 100,
      };
    }

    async function recalculate() {
      const btn = document.getElementById('btn-calc');
      const spinner = document.getElementById('calc-spinner');
      const btnText = document.getElementById('btn-calc-text');

      btn.disabled = true;
      btn.classList.add('calculating');
      spinner.style.display = 'block';
      btnText.textContent = 'Simulating…';
      document.getElementById('status-text').textContent = 'Running 2,000 MC paths…';

      try {
        const params = getSliderParams();
        const result = await postCalculate(params);
        renderAll(result);
        document.getElementById('status-text').textContent = 'Simulation complete ✓';
      } catch (err) {
        console.error('Recalculate error:', err);
        document.getElementById('status-text').textContent = '⚠️ Calculation error — check console';
      } finally {
        btn.disabled = false;
        btn.classList.remove('calculating');
        spinner.style.display = 'none';
        btnText.textContent = '⚡ Run Actuarial Simulation';
      }
    }

    function resetToBase() {
      if (!_baseData) return;

      const p = _baseData.params || {};
      const setSl = (id, val) => { const el = document.getElementById(id); if (el) el.value = val; };

      setSl('sl-age', p.current_age || 28);
      setSl('sl-ret-age', p.retirement_age || 60);
      setSl('sl-life', p.life_expectancy || 85);
      setSl('sl-sg', (p.salary_growth || 0.08) * 100);
      setSl('sl-inf', (p.inflation || 0.06) * 100);
      setSl('sl-elss-r', (p.elss_net_return || 0.12) * 100);
      setSl('sl-nps-r', (p.nps_blended_return || 0.1075) * 100);
      setSl('sl-epf-r', (p.epf_return || 0.0815) * 100);
      setSl('sl-elss-sip', p.elss_monthly_sip || 10_000);
      setSl('sl-nps-e', (p.nps_employee_pct || 0.05) * 100);
      setSl('sl-wc-e', (p.wecare_employee_pct || 0.10) * 100);
      setSl('sl-swr', (p.elss_swr || 0.04) * 100);
      setSl('sl-house-price', p.housing_house_price || 15000000);
      setSl('sl-down-payment-pct', (p.housing_down_payment_pct || 0.20) * 100);
      setSl('sl-loan-rate', (p.housing_loan_rate || 0.075) * 100);
      setSl('sl-loan-tenure', p.housing_loan_tenure || 20);
      setSl('sl-safe-emi-pct', (p.housing_safe_emi_pct || 0.35) * 100);
      document.getElementById('inp-ctc').value = p.starting_ctc || 2_000_000;

      document.getElementById('val-age').textContent = (p.current_age || 28) + ' yrs';
      document.getElementById('val-ret-age').textContent = (p.retirement_age || 60) + ' yrs';
      document.getElementById('val-life').textContent = (p.life_expectancy || 85) + ' yrs';
      document.getElementById('val-sg').textContent = ((p.salary_growth || 0.08) * 100).toFixed(1) + '%';
      document.getElementById('val-inf').textContent = ((p.inflation || 0.06) * 100).toFixed(1) + '%';
      document.getElementById('val-elss-r').textContent = ((p.elss_net_return || 0.12) * 100).toFixed(2) + '%';
      document.getElementById('val-nps-r').textContent = ((p.nps_blended_return || 0.1075) * 100).toFixed(2) + '%';
      document.getElementById('val-epf-r').textContent = ((p.epf_return || 0.0815) * 100).toFixed(2) + '%';
      document.getElementById('val-elss-sip').textContent = fmtINR(p.elss_monthly_sip || 10_000);
      document.getElementById('val-nps-e').textContent = ((p.nps_employee_pct || 0.05) * 100).toFixed(1) + '%';
      document.getElementById('val-wc-e').textContent = ((p.wecare_employee_pct || 0.10) * 100).toFixed(1) + '%';
      document.getElementById('val-swr').textContent = ((p.elss_swr || 0.04) * 100).toFixed(1) + '%';
      document.getElementById('val-house-price').textContent = fmtINR(p.housing_house_price || 15000000);
      document.getElementById('val-down-payment-pct').textContent = ((p.housing_down_payment_pct || 0.20) * 100).toFixed(1) + '%';
      document.getElementById('val-loan-rate').textContent = ((p.housing_loan_rate || 0.075) * 100).toFixed(2) + '%';
      document.getElementById('val-loan-tenure').textContent = (p.housing_loan_tenure || 20) + ' yrs';
      document.getElementById('val-safe-emi-pct').textContent = ((p.housing_safe_emi_pct || 0.35) * 100).toFixed(1) + '%';

      renderAll(_baseData);
      document.getElementById('status-text').textContent = 'Base case restored ✓';
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       EXPORT DATA FUNCTION (Fixed & Mapped to correct API JSON keys)
       ═══════════════════════════════════════════════════════════════════════════ */
    function exportData() {
      const activeData = _data || _baseData;
      if (!activeData) {
        alert("Projections are still computing, please wait.");
        return;
      }

      const sp = activeData.salary_proj || [];
      const cb = activeData.corpus_build || [];
      const ret = activeData.retirement || {};
      const p = activeData.params || {};
      const mc = activeData.monte_carlo || {};
      const h = activeData.housing || {};

      let csvContent = "";
      
      csvContent += "WealthBridge Executive Retirement Projections Report\\r\\n";
      csvContent += "Motto: Bridging Today's Income with Tomorrow's Retirement\\r\\n";
      csvContent += `Generated on: ${new Date().toLocaleString()}\\r\\n\\r\\n`;
      
      csvContent += "1. KEY RETIREMENT PROFILE & ASSUMPTIONS\\r\\n";
      csvContent += "Parameter,Value,Description\\r\\n";
      csvContent += `Current Age,${p.current_age} yrs,Rahul's starting age\\r\\n`;
      csvContent += `Retirement Age,${p.retirement_age} yrs,Target retirement age\\r\\n`;
      csvContent += `Starting Annual CTC,${p.starting_ctc} INR,Starting annual CTC compensation\\r\\n`;
      csvContent += `Salary Growth Rate,${(p.salary_growth * 100).toFixed(2)}%,Expected annual salary growth\\r\\n`;
      csvContent += `Inflation Rate (CPI),${(p.inflation * 100).toFixed(2)}%,Expected annual CPI inflation\\r\\n`;
      csvContent += `Life Expectancy,${p.life_expectancy} yrs,Survival calculation target\\r\\n`;
      csvContent += `EPF Return Rate,${(p.epf_return * 100).toFixed(2)}%,Expected annual yield on EPF\\r\\n`;
      csvContent += `NPS Return Rate,${(p.nps_blended_return * 100).toFixed(2)}%,Expected blended yield on NPS\\r\\n`;
      csvContent += `ELSS SIP Return Rate,${(p.elss_net_return * 100).toFixed(2)}%,Net yield on ELSS Equity SIP\\r\\n`;
      csvContent += `ELSS Safe Withdrawal Rate,${(p.elss_swr * 100).toFixed(2)}%,Safe drawdown SWR\\r\\n`;
      csvContent += `Income Tax Rate,${(p.income_tax_rate * 100).toFixed(2)}%,Effective rate on income\\r\\n\\r\\n`;

      if (h && h.house_price) {
        csvContent += "2. HOUSING AFFORDABILITY METRICS\\r\\n";
        csvContent += "Metric,Value,Threshold & Status\\r\\n";
        csvContent += `Target House Price,${h.house_price} INR,-\\r\\n`;
        csvContent += `Required Down Payment (INR),${h.down_payment_val} INR,${(h.down_payment_pct * 100).toFixed(1)}% of price\\r\\n`;
        csvContent += `Home Loan Amount,${h.loan_amount} INR,-\\r\\n`;
        csvContent += `Monthly Loan EMI,${h.monthly_emi} INR/month,-\\r\\n`;
        csvContent += `Safe EMI Limit,${h.safe_emi_limit} INR/month,${(p.housing_safe_emi_pct * 100).toFixed(1)}% of net income\\r\\n`;
        csvContent += `Affordability Verdict,${h.is_affordable ? "SAFE / AFFORDABLE" : "HIGH RISK / EXCEEDS LIMIT"},-\\r\\n`;
        csvContent += `Max Affordable House Price,${h.max_affordable_house_price} INR,Based on safe EMI threshold\\r\\n\\r\\n`;
      }

      csvContent += "3. CAREER HORIZON COMPREHENSIVE PROJECTIONS\\r\\n";
      csvContent += "Year,Age,Annual CTC,Monthly Net Take-Home,EPF Contributions/mo,NPS Employee Cont/mo,ELSS SIP/mo,EPF End-of-Yr Corpus,NPS End-of-Yr Corpus,ELSS End-of-Yr Corpus,WeCare Cumulative/mo,Total Accumulated Corpus\\r\\n";
      
      for (let i = 0; i < sp.length; i++) {
        const s = sp[i];
        const c = cb[i] || {};
        csvContent += `${s.year},${s.age},${s.annual_ctc},${s.net_takehome_pm},${s.epf_total_pm},${s.nps_emp_pm},${s.elss_sip_pm},${c.epf_corpus || 0},${c.nps_corpus || 0},${c.elss_corpus || 0},${c.wecare_cumul || 0},${c.total_corpus || 0}\\r\\n`;
      }
      csvContent += "\\r\\n";

      csvContent += "4. RETIRETMENT OUTCOMES & CASH FLOWS AT AGE 60\\r\\n";
      csvContent += "Income Stream / Asset,Monthly Retirement Income,Total Available Lump Sum\\r\\n";
      csvContent += `EPF Monthly Annuity (Nominal),${ret.epf_monthly_annuity || 0},-\\r\\n`;
      csvContent += `NPS Monthly Annuity (Nominal),${ret.nps_monthly_annuity || 0},${ret.nps_lumpsum || 0} (60% Tax-Free)\\r\\n`;
      csvContent += `WeCare DB Pension (Pre-commuted),${ret.wecare_monthly_pre || 0},${ret.wecare_commuted_lumpsum || 0} (33% Commuted)\\r\\n`;
      csvContent += `ELSS 4% SWR Sustainable Drawdown,${ret.elss_monthly_swr || 0},${ret.elss_corpus_full || 0} (100% Flexible)\\r\\n`;
      csvContent += `TOTAL MONTHLY RETIREMENT CASH FLOW,${ret.total_monthly_income || 0},-\\r\\n`;
      csvContent += `Final Month CTC (Pre-retirement),${ret.final_monthly_ctc || 0},-\\r\\n`;
      csvContent += `Actuarial Replacement Ratio,${ret.replacement_ratio || 0}%,Target: 50% to 70%\\r\\n`;
      csvContent += `Total Invested Capital,${ret.total_invested || 0},-\\r\\n`;
      csvContent += `Total Compound Growth Returns,${ret.total_returns || 0},-\\r\\n`;
      csvContent += `Total Accumulated Corpus at Retirement,${ret.total_corpus || 0},-\\r\\n`;
      csvContent += `Monte Carlo Survival Probability to Age ${mc.life_expectancy || 85},${mc.success_probability || 0}%,Based on 2000 random market paths\\r\\n`;

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.setAttribute("href", url);
      link.setAttribute("download", `WealthBridge_Retirement_Report_${p.current_age}_to_${p.retirement_age}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       TAB SWITCHING
       ═══════════════════════════════════════════════════════════════════════════ */
    function switchTab(n) {
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
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       BOOTSTRAP ON LOAD
       ═══════════════════════════════════════════════════════════════════════════ */
    document.addEventListener('DOMContentLoaded', async () => {
      // 1. Initialize Canvas-based Guilloche Wave Animation (Bright/Beige full screen)
      const canvas = document.getElementById('startup-canvas');
      let drawActive = true;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        const resizeCanvas = () => {
          canvas.width = window.innerWidth;
          canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        let timeVal = 0;
        const drawGuilloche = () => {
          if (!drawActive) return;
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          
          // Render beautiful linear bright background gradient
          const bgGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
          bgGrad.addColorStop(0, '#FAF8F5');
          bgGrad.addColorStop(1, '#F3EFE9');
          ctx.fillStyle = bgGrad;
          ctx.fillRect(0, 0, canvas.width, canvas.height);

          const cy = canvas.height / 2;
          timeVal += 0.005;
          
          // Draw 12 waves spanning the whole screen vertically
          for (let w = 0; w < 12; w++) {
            ctx.beginPath();
            ctx.lineWidth = 0.8;
            
            // Warm beige strokes with subtle transparency shifts
            const alpha = 0.12 + 0.10 * Math.sin(timeVal * 0.8 + w * 0.5);
            ctx.strokeStyle = `rgba(210, 180, 140, ${alpha})`;
            
            const offset = (w - 5.5) * (canvas.height / 9.5); // distribute evenly from top to bottom
            
            for (let x = 0; x < canvas.width; x += 3) {
              const carrier = Math.sin(x * 0.0016 + timeVal * 0.35 + w * 0.45);
              const mod1 = Math.sin(x * 0.012 + timeVal * 1.1 + w * Math.PI / 3.2);
              const mod2 = Math.cos(x * 0.030 - timeVal * 1.6 + w * Math.PI / 5.8);
              
              const y = cy + offset + carrier * 90 + mod1 * 18 + mod2 * 6;
              
              if (x === 0) ctx.moveTo(x, y);
              else ctx.lineTo(x, y);
            }
            ctx.stroke();
          }
          requestAnimationFrame(drawGuilloche);
        };
        drawGuilloche();
      }

      // 2. Initialize Theme from localStorage (Default to Bright/Light mode)
      const savedTheme = localStorage.getItem('theme') || 'light';
      if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        const btnIcon = document.querySelector('.theme-toggle-icon');
        const btnText = document.querySelector('.theme-toggle-text');
        if (btnIcon) btnIcon.textContent = '🌙';
        if (btnText) btnText.textContent = 'Dark Mode';
        updateChartThemeDefaults(true);
      } else {
        document.body.classList.remove('light-mode');
        const btnIcon = document.querySelector('.theme-toggle-icon');
        const btnText = document.querySelector('.theme-toggle-text');
        if (btnIcon) btnIcon.textContent = '☀️';
        if (btnText) btnText.textContent = 'Bright Mode';
        updateChartThemeDefaults(false);
      }

      const startTime = Date.now();
      const progressBar = document.getElementById('startup-progress');
      const statusText = document.getElementById('startup-status');
      
      let progress = 0;
      const progressInterval = setInterval(() => {
        if (progress < 90) {
          progress += Math.floor(Math.random() * 8) + 4;
          if (progress > 90) progress = 90;
          progressBar.style.width = progress + '%';
          
          if (progress < 30) {
            statusText.textContent = 'Initializing WealthBridge Engine...';
          } else if (progress < 60) {
            statusText.textContent = 'Connecting to actuarial database...';
          } else {
            statusText.textContent = 'Running 2,000 Monte Carlo simulations...';
          }
        }
      }, 120);

      try {
        const data = await fetchBaseData();
        _baseData = data;
        renderAll(data);
        document.getElementById('status-text').textContent = 'Base case loaded ✓';
        statusText.textContent = 'Calculations complete!';
        
        const elapsed = Date.now() - startTime;
        const remaining = Math.max(0, 3000 - elapsed);
        
        setTimeout(() => {
          clearInterval(progressInterval);
          progressBar.style.width = '100%';
          statusText.textContent = 'Ready!';
          
          setTimeout(() => {
            const startupScreen = document.getElementById('startup-screen');
            if (startupScreen) {
              startupScreen.style.opacity = '0';
              startupScreen.style.transition = 'opacity 0.8s cubic-bezier(0.25, 1, 0.5, 1)';
              
              setTimeout(() => {
                startupScreen.style.display = 'none';
                drawActive = false; // Stop canvas loops to conserve CPU resources
              }, 800);
            }
          }, 300);
        }, remaining);

      } catch (err) {
        console.error('Bootstrap loader error:', err);
        clearInterval(progressInterval);
        statusText.textContent = '⚠️ Connection failed';
        if (progressBar) progressBar.style.backgroundColor = 'var(--magenta)';
        
        const bannerText = document.getElementById('status-text');
        if (bannerText) bannerText.textContent = '⚠️ API connection error';
        
        alert("WealthBridge Actuarial Server is not running. Please make sure uvicorn is running on port 8000.");
      }
    });
  </script>
</body>

</html>
"""

# Write it directly as a clean utf-8 file to templates/index.html
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully rewrote templates/index.html with Bright-Default, Beige canvas, and Aqua themes!")
