import sys
import os
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath("api"))
import index

D = Decimal
ZERO = D("0")
R2 = D("0.01")
R0 = D("1")

def to_d(v) -> Decimal:
    return D(str(v))

def r0(d: Decimal) -> float:
    return float(d.quantize(R0, rounding=ROUND_HALF_UP))

# Force the new filenames in index
index._CSV_NAMES = {
    "assumptions": "WeCare_Financial_Model-1(ASSUMPTIONS).csv",
    "salary":      "WeCare_Financial_Model-1(SALARY_PROJ).csv",
    "corpus":      "WeCare_Financial_Model-1(CORPUS_BUILD).csv",
    "retirement":  "WeCare_Financial_Model-1(RETIREMENT).csv",
}
p = index.load_assumptions()

years = int(p["retirement_age"] - p["current_age"])
starting_ctc = to_d(p["starting_ctc"])
basic_pct = to_d(p["basic_pct"])
salary_growth = to_d(p["salary_growth"])
income_tax = to_d(p["income_tax_rate"])

epf_emp_r = to_d(p["epf_employee_rate"])
epf_empr_r = to_d(p["epf_employer_rate"])
epf_ret = to_d(p["epf_return"])

nps_emp_r = to_d(p["nps_employee_pct"])
nps_empr_r = to_d(p["nps_employer_pct"])
nps_ret = to_d(p["nps_blended_return"])

elss_sip_start = to_d(p["elss_monthly_sip"])
elss_stepup = to_d(p["elss_stepup"])
elss_ret = to_d(p["elss_net_return"])

wc_emp_r = to_d(p["wecare_employee_pct"])
wc_pen_pct = to_d(p["wecare_pension_pct"])
comm_factor = to_d(p["commutation_factor"])

epf_corpus = ZERO
nps_corpus = ZERO
elss_corpus = ZERO
wc_cumul = ZERO

elss_monthly_cur = elss_sip_start

df_cb = pd.read_csv("WeCare_Financial_Model-1(CORPUS_BUILD).csv", skiprows=3, header=None, encoding='latin1').dropna(subset=[0])
# Filter out non-digit rows in Col 0
df_cb = df_cb[df_cb[0].astype(str).str.strip().str.isdigit()]

print("Checking year-by-year values:")
for yr in range(1, years + 1):
    age = int(p["current_age"]) + yr - 1
    
    growth_factor = (D("1") + salary_growth) ** (yr - 1)
    ctc = starting_ctc * growth_factor
    basic_pa = ctc * basic_pct
    basic_pm = basic_pa / D("12")
    
    # Monthly deductions for Take-Home
    epf_emp_pm = basic_pm * epf_emp_r
    epf_empr_pm = basic_pm * epf_empr_r
    nps_emp_pm = basic_pm * nps_emp_r
    nps_empr_pm = basic_pm * nps_empr_r
    wc_pm = basic_pm * wc_emp_r
    
    if yr > 1:
        elss_monthly_cur = elss_monthly_cur * (D("1") + elss_stepup)
    
    # Annual contribution added to Corpus in CORPUS_BUILD (doubled in sheet)
    epf_annual = (epf_emp_pm + epf_empr_pm) * D("24") # doubled
    nps_annual = (nps_emp_pm + nps_empr_pm) * D("12") # single
    elss_annual = elss_monthly_cur * D("12")          # single
    wc_annual = wc_pm * D("24")                       # doubled
    
    if yr == 1:
        epf_corpus  = epf_annual  * (D("1") + epf_ret)
        nps_corpus  = nps_annual  * (D("1") + nps_ret)
        elss_corpus = elss_annual * (D("1") + elss_ret)
        wc_cumul    = wc_annual * to_d("1.0875")
    else:
        epf_corpus  = epf_corpus  * (D("1") + epf_ret)  + epf_annual
        nps_corpus  = nps_corpus  * (D("1") + nps_ret)  + nps_annual
        elss_corpus = elss_corpus * (D("1") + elss_ret) + elss_annual
        wc_cumul    = wc_cumul * to_d("1.0875") + wc_annual
    
    total_c = epf_corpus + nps_corpus + elss_corpus + wc_cumul
    
    # Let's compare with CSV row for this year
    csv_row = df_cb.iloc[yr - 1]
    csv_epf_ann = float(str(csv_row.iloc[2]).replace(',', ''))
    csv_epf_corp = float(str(csv_row.iloc[3]).replace(',', ''))
    csv_wc_ann = float(str(csv_row.iloc[8]).replace(',', ''))
    csv_wc_cum = float(str(csv_row.iloc[9]).replace(',', ''))
    csv_total = float(str(csv_row.iloc[10]).replace(',', ''))
    
    if yr in (1, 10, 20, 32):
        print(f"\nYear {yr} (Age {age}):")
        print(f"  EPF Ann: Calc={r0(epf_annual):,} vs CSV={csv_epf_ann:,}")
        print(f"  EPF Corp: Calc={r0(epf_corpus):,} vs CSV={csv_epf_corp:,}")
        print(f"  WeCare Ann: Calc={r0(wc_annual):,} vs CSV={csv_wc_ann:,}")
        print(f"  WeCare Cum: Calc={r0(wc_cumul):,} vs CSV={csv_wc_cum:,}")
        print(f"  Total Corp: Calc={r0(total_c):,} vs CSV={csv_total:,}")
