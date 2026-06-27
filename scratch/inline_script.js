
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
      // Indian number system: last 3 digits, then groups of 2
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
    Chart.defaults.color = '#A0A0B0';
    Chart.defaults.borderColor = 'rgba(157,78,221,0.12)';
    Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(22,22,31,0.95)';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(157,78,221,0.40)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.titleColor = '#F0F0F5';
    Chart.defaults.plugins.tooltip.bodyColor = '#A0A0B0';
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    Chart.defaults.plugins.tooltip.callbacks = {
      label: ctx => {
        const v = ctx.parsed.y ?? ctx.parsed;
        return typeof v === 'number' ? '  ' + fmtINR(v, true) : '  ' + v;
      }
    };

    function updateChartThemeDefaults(isLight) {
      Chart.defaults.color = isLight ? '#665D55' : '#A0A0B0';
      Chart.defaults.borderColor = isLight ? 'rgba(122,63,168,0.15)' : 'rgba(157,78,221,0.12)';
      Chart.defaults.plugins.tooltip.backgroundColor = isLight ? 'rgba(252,250,247,0.95)' : 'rgba(22,22,31,0.95)';
      Chart.defaults.plugins.tooltip.borderColor = isLight ? 'rgba(122,63,168,0.40)' : 'rgba(157,78,221,0.40)';
      Chart.defaults.plugins.tooltip.titleColor = isLight ? '#2C2621' : '#F0F0F5';
      Chart.defaults.plugins.tooltip.bodyColor = isLight ? '#665D55' : '#A0A0B0';
    }

    function toggleTheme() {
      const isLight = document.body.classList.toggle('light-mode');
      localStorage.setItem('theme', isLight ? 'light' : 'dark');

      const btnIcon = document.querySelector('.theme-toggle-icon');
      const btnText = document.querySelector('.theme-toggle-text');
      if (btnIcon) btnIcon.textContent = isLight ? '🌙' : '☀️';
      if (btnText) btnText.textContent = isLight ? 'Dark Mode' : 'Bright Mode';

      // Update Chart.js defaults
      updateChartThemeDefaults(isLight);

      // Force update existing charts
      const gridColorX = isLight ? 'rgba(122,63,168,0.06)' : 'rgba(157,78,221,0.06)';
      const gridColorY = isLight ? 'rgba(122,63,168,0.08)' : 'rgba(157,78,221,0.08)';
      const tickColor = isLight ? '#665D55' : '#A0A0B0';
      const labelColor = isLight ? '#665D55' : '#A0A0B0';

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
        _charts.donut.data.datasets[0].borderColor = isLight ? '#FCFAF5' : '#16161F';
        _charts.donut.update();
      }
      if (_charts.corpus) {
        _charts.corpus.options.scales.x.grid.color = isLight ? 'rgba(122,63,168,0.05)' : 'rgba(157,78,221,0.05)';
        _charts.corpus.options.scales.x.ticks.color = tickColor;
        _charts.corpus.options.scales.y.grid.color = isLight ? 'rgba(122,63,168,0.07)' : 'rgba(157,78,221,0.07)';
        _charts.corpus.options.scales.y.ticks.color = tickColor;
        _charts.corpus.options.plugins.legend.labels.color = labelColor;
        _charts.corpus.update();
      }
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       CHART INITIALISATION HELPERS
    ═══════════════════════════════════════════════════════════════════════════ */
    function makeAreaFill(hex, alpha) {
      return function (context) {
        const chart = context.chart;
        const { ctx, chartArea } = chart;
        if (!chartArea) return hex;
        const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
        gradient.addColorStop(0, hex + Math.round(alpha * 255).toString(16).padStart(2, '0'));
        gradient.addColorStop(1, hex + '00');
        return gradient;
      };
    }

    /* ── Monte Carlo P10/P50/P90 Chart ─────────────────────────────────────── */
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
              borderColor: '#C77DFF',
              borderWidth: 1.5,
              pointRadius: 0,
              tension: 0.4,
              fill: '+1',
              backgroundColor: (ctx) => {
                const chart = ctx.chart;
                const { ctx: c, chartArea } = chart;
                if (!chartArea) return 'rgba(199,125,255,0.10)';
                const g = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                g.addColorStop(0, 'rgba(199,125,255,0.18)');
                g.addColorStop(1, 'rgba(199,125,255,0.02)');
                return g;
              },
            },
            {
              label: 'P50 — Expected Median',
              data: p50,
              borderColor: '#9D4EDD',
              borderWidth: 2.5,
              pointRadius: 0,
              tension: 0.4,
              fill: '+1',
              backgroundColor: (ctx) => {
                const chart = ctx.chart;
                const { ctx: c, chartArea } = chart;
                if (!chartArea) return 'rgba(157,78,221,0.10)';
                const g = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                g.addColorStop(0, 'rgba(157,78,221,0.16)');
                g.addColorStop(1, 'rgba(157,78,221,0.02)');
                return g;
              },
            },
            {
              label: 'P10 — Pessimistic',
              data: p10,
              borderColor: '#7C3AED',
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
              grid: { color: isLight ? 'rgba(122,63,168,0.06)' : 'rgba(157,78,221,0.06)' },
              ticks: {
                color: isLight ? '#665D55' : '#606070', maxTicksLimit: 12,
                callback: v => 'Yr ' + (v + 1) + '\n(Age ' + ages[v] + ')'
              }
            },
            y: {
              grid: { color: isLight ? 'rgba(122,63,168,0.08)' : 'rgba(157,78,221,0.08)' },
              ticks: {
                color: isLight ? '#665D55' : '#A0A0B0',
                callback: v => fmtINR(v, true),
              }
            }
          }
        }
      });
    }

    /* ── Salary Bar Chart ──────────────────────────────────────────────────── */
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
              backgroundColor: 'rgba(157,78,221,0.70)',
              borderColor: '#9D4EDD',
              borderWidth: 1,
              borderRadius: 3,
            },
            {
              label: 'Annual Net Take-Home',
              data: thData,
              backgroundColor: 'rgba(79,195,247,0.65)',
              borderColor: '#4FC3F7',
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
              labels: { boxWidth: 10, padding: 16, color: isLight ? '#665D55' : '#A0A0B0', font: { size: 11 } }
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
              ticks: { color: isLight ? '#665D55' : '#606070', maxTicksLimit: 10, font: { size: 10 } }
            },
            y: {
              grid: { color: isLight ? 'rgba(122,63,168,0.06)' : 'rgba(157,78,221,0.06)' },
              ticks: { color: isLight ? '#665D55' : '#A0A0B0', callback: v => fmtINR(v, true) }
            }
          }
        }
      });
    }

    /* ── Donut Chart ───────────────────────────────────────────────────────── */
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
              'rgba(79,195,247,0.80)',
              'rgba(157,78,221,0.80)',
              'rgba(224,30,55,0.80)',
              'rgba(255,152,0,0.80)',
              'rgba(255,215,0,0.80)',
            ],
            borderColor: isLight ? '#FCFAF5' : '#16161F',
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

      // Update donut legend
      const legendData = [
        { label: 'EPF Invested', val: epfInv, color: '#4FC3F7' },
        { label: 'NPS Invested', val: npsInv, color: '#9D4EDD' },
        { label: 'ELSS Invested', val: elssInv, color: '#E01E37' },
        { label: 'WeCare Invested', val: wcInv, color: '#FF9800' },
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

    /* ── Corpus Curves Chart ───────────────────────────────────────────────── */
    function initCorpusChart(corpusBuild) {
      const ctx = document.getElementById('chart-corpus').getContext('2d');
      if (_charts.corpus) _charts.corpus.destroy();

      const isLight = document.body.classList.contains('light-mode');

      const labels = corpusBuild.map(r => 'Age ' + r.age);

      const makeGrad = (hex) => (ctx) => {
        const chart = ctx.chart;
        const { ctx: c, chartArea } = chart;
        if (!chartArea) return hex + '20';
        const g = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
        g.addColorStop(0, hex + '30');
        g.addColorStop(1, hex + '04');
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
              borderColor: '#4FC3F7',
              backgroundColor: makeGrad('#4FC3F7'),
              borderWidth: 2, pointRadius: 0, tension: 0.4, fill: true,
            },
            {
              label: 'NPS',
              data: corpusBuild.map(r => r.nps_corpus),
              borderColor: '#9D4EDD',
              backgroundColor: makeGrad('#9D4EDD'),
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
              borderColor: '#FF9800',
              backgroundColor: makeGrad('#FF9800'),
              borderWidth: 2, pointRadius: 0, tension: 0.4, fill: true,
            },
            {
              label: 'Total',
              data: corpusBuild.map(r => r.total_corpus),
              borderColor: '#FFD700',
              backgroundColor: 'transparent',
              borderWidth: 3, pointRadius: 0, tension: 0.4, fill: false,
              borderDash: [0],
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
              labels: { boxWidth: 10, padding: 16, color: isLight ? '#665D55' : '#A0A0B0', font: { size: 11 } }
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
              grid: { color: isLight ? 'rgba(122,63,168,0.05)' : 'rgba(157,78,221,0.05)' },
              ticks: { color: isLight ? '#665D55' : '#606070', maxTicksLimit: 12, font: { size: 10 } }
            },
            y: {
              grid: { color: isLight ? 'rgba(122,63,168,0.07)' : 'rgba(157,78,221,0.07)' },
              ticks: { color: isLight ? '#665D55' : '#A0A0B0', callback: v => fmtINR(v, true) }
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

      // Tab 1 metrics
      document.getElementById('m-corpus').textContent = fmtINR(ret.total_corpus, true);
      document.getElementById('m-income').textContent = fmtINR(ret.total_monthly_income);
      const rr = parseFloat(ret.replacement_ratio);
      const rrEl = document.getElementById('m-rr');
      rrEl.textContent = fmtPct(rr);
      if (rr >= 70) { rrEl.style.color = 'var(--green)'; document.getElementById('m-rr-sub').textContent = '✅ Exceeds 70% target'; }
      else if (rr >= 50) { rrEl.style.color = 'var(--purple)'; document.getElementById('m-rr-sub').textContent = '✅ On-Track (50%–70%)'; }
      else { rrEl.style.color = 'var(--magenta)'; document.getElementById('m-rr-sub').textContent = '⚠️ Below 50% target'; }

      // Success probability callout
      const sp = mc.success_probability;
      document.getElementById('success-prob').innerHTML = sp.toFixed(1) + '<span class="pct-sign">%</span>';
      document.getElementById('callout-age').textContent = 'age ' + mc.life_expectancy;
      const tag = document.getElementById('prob-tag');
      if (sp >= 85) { tag.className = 'tag green'; tag.textContent = '✅ High Confidence'; }
      else if (sp >= 60) { tag.className = 'tag amber'; tag.textContent = '⚠️ Moderate Risk'; }
      else { tag.className = 'tag red'; tag.textContent = '🚨 High Depletion Risk'; }

      // Tab 2 summary rows
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

      // Tab 3 corpus cards
      document.getElementById('wc-epf').textContent = fmtINR(ret.epf_corpus, true);
      document.getElementById('wc-nps').textContent = fmtINR(ret.nps_corpus, true);
      document.getElementById('wc-elss').textContent = fmtINR(ret.elss_corpus, true);
      document.getElementById('wc-wecare').textContent = fmtINR(ret.wecare_corpus, true);

      // Tab 3 income rows
      document.getElementById('ri-epf').textContent = fmtINR(ret.epf_monthly_annuity) + ' / mo';
      document.getElementById('ri-nps').textContent = fmtINR(ret.nps_monthly_annuity) + ' / mo';
      document.getElementById('ri-wecare').textContent = fmtINR(ret.wecare_monthly_pre) + ' / mo';
      document.getElementById('ri-elss').textContent = fmtINR(ret.elss_monthly_swr) + ' / mo';
      document.getElementById('ri-total').textContent = fmtINR(ret.total_monthly_income) + ' / mo';
      document.getElementById('ri-rr').textContent = fmtPct(ret.replacement_ratio) + ' of Final Salary';

      // Lump sums
      document.getElementById('ls-nps').textContent = fmtINR(ret.nps_lumpsum, true);
      document.getElementById('ls-wc').textContent = fmtINR(ret.wecare_commuted_lumpsum, true);
      document.getElementById('ls-elss').textContent = fmtINR(ret.elss_corpus_full, true);
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
      // Ensure accumulation period is at least 1 year
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
        // Fixed plan parameters (always pass through)
        wecare_employee_pct: g('sl-wc-e') / 100,
        wecare_pension_pct: 0.50,
        wecare_commutation_pct: 0.33,
        commutation_factor: 11.0,
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

      // Reset sliders and inputs to base-case values
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
      document.getElementById('inp-ctc').value = p.starting_ctc || 2_000_000;

      // Refresh display labels
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

      renderAll(_baseData);
      document.getElementById('status-text').textContent = 'Base case restored ✓';
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

      // Trigger chart resize on tab switch (charts may be hidden during init)
      setTimeout(() => {
        Object.values(_charts).forEach(c => { if (c) c.resize(); });
      }, 80);
    }

    /* ═══════════════════════════════════════════════════════════════════════════
       BOOTSTRAP ON LOAD
    ═══════════════════════════════════════════════════════════════════════════ */
    document.addEventListener('DOMContentLoaded', async () => {
      // Initialize theme from localStorage
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        const btnIcon = document.querySelector('.theme-toggle-icon');
        const btnText = document.querySelector('.theme-toggle-text');
        if (btnIcon) btnIcon.textContent = '🌙';
        if (btnText) btnText.textContent = 'Dark Mode';
        updateChartThemeDefaults(true);
      }

      try {
        const data = await fetchBaseData();
        _baseData = data;
        renderAll(data);
        document.getElementById('status-text').textContent = 'Base case loaded ✓';
      } catch (err) {
        console.error('Bootstrap error:', err);
        document.getElementById('status-text').textContent = '⚠️ API unavailable — check server';
        document.getElementById('loading-overlay').querySelector('.loading-text').textContent =
          '⚠️ Could not connect to the actuarial engine. Make sure the FastAPI server is running.';
        return;
      } finally {
        const overlay = document.getElementById('loading-overlay');
        overlay.classList.add('hidden');
        setTimeout(() => { overlay.style.display = 'none'; }, 500);
      }
    });
  