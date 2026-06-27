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

def r2(d: Decimal) -> float:
    return float(d.quantize(R2, rounding=ROUND_HALF_UP))

# Force the new filenames in index
index._CSV_NAMES = {
    "assumptions": "WeCare_Financial_Model-1(ASSUMPTIONS).csv",
    "salary":      "WeCare_Financial_Model-1(SALARY_PROJ).csv",
    "corpus":      "WeCare_Financial_Model-1(CORPUS_BUILD).csv",
    "retirement":  "WeCare_Financial_Model-1(RETIREMENT).csv",
}
p = index.load_assumptions()

def compute_projections_modified(p: dict) -> dict:
    years          = int(to_d(p["retirement_age"]) - to_d(p["current_age"]))
    starting_ctc   = to_d(p["starting_ctc"])
    basic_pct      = to_d(p["basic_pct"])
    salary_growth  = to_d(p["salary_growth"])
    income_tax     = to_d(p["income_tax_rate"])

    epf_emp_r      = to_d(p["epf_employee_rate"])
    epf_empr_r     = to_d(p["epf_employer_rate"])
    epf_ret        = to_d(p["epf_return"])

    nps_emp_r      = to_d(p["nps_employee_pct"])
    nps_empr_r     = to_d(p["nps_employer_pct"])
    nps_ret        = to_d(p["nps_blended_return"])
    nps_ann_pct    = to_d(p["nps_annuity_pct"])
    nps_ann_rate   = to_d(p["nps_annuity_rate"])

    elss_sip_start = to_d(p["elss_monthly_sip"])
    elss_stepup    = to_d(p["elss_stepup"])
    elss_ret       = to_d(p["elss_net_return"])
    elss_swr       = to_d(p["elss_swr"])

    wc_emp_r       = to_d(p["wecare_employee_pct"])
    wc_pen_pct     = to_d(p["wecare_pension_pct"])
    wc_comm_pct    = to_d(p["wecare_commutation_pct"])
    comm_factor    = to_d(p["commutation_factor"])

    # Running corpus balances
    epf_corpus     = ZERO
    nps_corpus     = ZERO
    elss_corpus    = ZERO
    wc_cumul       = ZERO

    elss_monthly_cur = elss_sip_start

    salary_proj:  list[dict] = []
    corpus_build: list[dict] = []
    final_basic_pm = ZERO

    for yr in range(1, years + 1):
        age = int(p["current_age"]) + yr - 1

        growth_factor = (D("1") + salary_growth) ** (yr - 1)
        ctc           = starting_ctc * growth_factor
        basic_pa      = ctc * basic_pct
        basic_pm      = basic_pa / D("12")

        # -- Salary deductions (single) ---------------------------------------
        epf_emp_pm  = basic_pm * epf_emp_r
        epf_empr_pm = basic_pm * epf_empr_r
        epf_annual  = (epf_emp_pm + epf_empr_pm) * D("24") # doubled in corpus

        # -- NPS (single) ---------------------------------------------
        nps_emp_pm  = basic_pm * nps_emp_r
        nps_empr_pm = basic_pm * nps_empr_r
        nps_annual  = (nps_emp_pm + nps_empr_pm) * D("12")

        # -- WeCare DB (doubled in corpus) ---
        wc_pm      = basic_pm * wc_emp_r
        wc_annual  = wc_pm * D("24") # doubled

        # -- ELSS SIP -------------------------------------
        if yr > 1:
            elss_monthly_cur = elss_monthly_cur * (D("1") + elss_stepup)
        elss_annual = elss_monthly_cur * D("12")

        # -- Corpus end-of-year compounding ------------------------------------
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
        
        total_c     = epf_corpus + nps_corpus + elss_corpus + wc_cumul

        # -- Net Take-Home -----------------------------------------------------
        gross_pm     = ctc / D("12")
        tax_pm       = gross_pm * income_tax
        # Deductions are correct (single contributions)
        net_takehome = gross_pm - tax_pm - epf_emp_pm - nps_emp_pm - wc_pm - elss_monthly_cur

        if yr == years:
            final_basic_pm = basic_pm

        salary_proj.append({
            "year":            yr,
            "age":             age,
            "annual_ctc":      r0(ctc),
            "basic_pa":        r0(basic_pa),
            "basic_pm":        r0(basic_pm),
            "epf_emp_pm":      r0(epf_emp_pm),
            "epf_empr_pm":     r0(epf_empr_pm),
            "epf_total_pm":    r0(epf_emp_pm + epf_empr_pm),
            "nps_emp_pm":      r0(nps_emp_pm),
            "nps_empr_pm":     r0(nps_empr_pm),
            "wecare_pm":       r0(wc_pm),
            "elss_sip_pm":     r0(elss_monthly_cur),
            "income_tax_pm":   r0(tax_pm),
            "net_takehome_pm": r0(net_takehome),
        })

        corpus_build.append({
            "year":          yr,
            "age":           age,
            "epf_annual":    r0(epf_annual),
            "epf_corpus":    r0(epf_corpus),
            "nps_annual":    r0(nps_annual),
            "nps_corpus":    r0(nps_corpus),
            "elss_annual":   r0(elss_annual),
            "elss_corpus":   r0(elss_corpus),
            "wecare_corpus": r0(wc_cumul),
            "total_corpus":  r0(total_c),
            "wecare_annual": r0(wc_annual),
            "wecare_cumul":  r0(wc_cumul),
        })

    # -- Retirement Outcome Metrics --------------------------------------------
    last = corpus_build[-1]
    epf_c  = to_d(str(last["epf_corpus"]))
    nps_c  = to_d(str(last["nps_corpus"]))
    elss_c = to_d(str(last["elss_corpus"]))
    wc_cum = to_d(str(last["wecare_cumul"]))

    # WeCare Defined Benefit pension (employer obligation)
    wc_monthly_pre   = final_basic_pm * wc_pen_pct          # 50% of final monthly basic
    wc_annual_pen    = wc_monthly_pre * D("12")
    wc_commuted_ann  = wc_annual_pen * wc_comm_pct           # 33% of annual commuted
    wc_lumpsum       = wc_commuted_ann * comm_factor         # 11x = lump sum
    wc_monthly_post  = wc_monthly_pre * (D("1") - wc_comm_pct)  # Remaining recurring

    # Capitalised pre-commutation WeCare corpus equivalent
    wecare_corpus    = wc_annual_pen * comm_factor
    total_c          = epf_c + nps_c + elss_c + wc_cum

    # EPF monthly income via 5.5% p.a. annuity
    epf_monthly_ann  = epf_c * nps_ann_rate / D("12")

    # NPS split: 40% annuity, 60% lump sum
    nps_lumpsum      = nps_c * (D("1") - nps_ann_pct)
    nps_ann_corpus   = nps_c * nps_ann_pct
    nps_monthly_ann  = nps_ann_corpus * nps_ann_rate / D("12")

    # ELSS 4% SWR monthly
    elss_monthly_swr = elss_c * elss_swr / D("12")

    # Total monthly retirement income (EPF annuity + NPS annuity + WeCare DB pension pre-commutation + ELSS SWR)
    total_monthly    = epf_monthly_ann + nps_monthly_ann + wc_monthly_pre + elss_monthly_swr

    # Replacement ratio vs final gross monthly CTC
    last_sal          = salary_proj[-1]
    final_monthly_ctc = to_d(str(last_sal["annual_ctc"])) / D("12")
    replacement_ratio = r2(total_monthly / final_monthly_ctc * D("100"))

    # Corpus breakdown: invested vs compound returns
    total_epf_inv  = r0(to_d(str(sum(r["epf_annual"]  for r in corpus_build))))
    total_nps_inv  = r0(to_d(str(sum(r["nps_annual"]  for r in corpus_build))))
    total_elss_inv = r0(to_d(str(sum(r["elss_annual"] for r in corpus_build))))
    total_invested = total_epf_inv + total_nps_inv + total_elss_inv + r0(wc_cum)
    total_returns  = r0(total_c) - total_invested

    retirement = {
        # Corpus
        "epf_corpus":             r0(epf_c),
        "nps_corpus":             r0(nps_c),
        "elss_corpus":            r0(elss_c),
        "wecare_corpus":          r0(wecare_corpus),
        "total_corpus":           r0(total_c),
        "wecare_cumul_emp":       r0(wc_cum),
        # Final salary
        "final_annual_ctc":       last_sal["annual_ctc"],
        "final_monthly_ctc":      r0(final_monthly_ctc),
        "final_annual_basic":     last_sal["basic_pa"],
        "final_monthly_basic":    r0(final_basic_pm),
        # Income streams
        "epf_monthly_annuity":    r0(epf_monthly_ann),
        "nps_lumpsum":            r0(nps_lumpsum),
        "nps_monthly_annuity":    r0(nps_monthly_ann),
        "elss_corpus_full":       r0(elss_c),
        "elss_monthly_swr":       r0(elss_monthly_swr),
        # WeCare DB
        "wecare_monthly_pre":     r0(wc_monthly_pre),
        "wecare_annual_pension":  r0(wc_annual_pen),
        "wecare_commuted_lumpsum":r0(wc_lumpsum),
        "wecare_monthly_post":    r0(wc_monthly_post),
        # Summary
        "total_monthly_income":   r0(total_monthly),
        "replacement_ratio":      replacement_ratio,
        # Invested vs Returns breakdown
        "total_epf_invested":     total_epf_inv,
        "total_nps_invested":     total_nps_inv,
        "total_elss_invested":    total_elss_inv,
        "total_invested":         total_invested,
        "total_returns":          total_returns,
    }

    return {
        "salary_proj":  salary_proj,
        "corpus_build": corpus_build,
        "retirement":   retirement,
    }

res = compute_projections_modified(p)
calc_ret = res["retirement"]
print("\n--- NEW COMPARISONS ---")
print(f"EPF Corpus: Calc={calc_ret['epf_corpus']:,} vs CSV 136,812,184")
print(f"NPS Corpus: Calc={calc_ret['nps_corpus']:,} vs CSV 63,600,530")
print(f"ELSS Corpus: Calc={calc_ret['elss_corpus']:,} vs CSV 99,290,891")
print(f"WeCare Employee Cumulative Contrib: Calc={calc_ret['wecare_cumul_emp']:,} vs CSV 62,258,019")
print(f"Total Investable Corpus: Calc={calc_ret['total_corpus']:,} vs CSV 361,961,624")

print(f"\nFinal Salary (Annual CTC): Calc={calc_ret['final_annual_ctc']:,} vs CSV 21,735,339")
print(f"Final Salary (Monthly CTC): Calc={calc_ret['final_monthly_ctc']:,} vs CSV 1,811,278")
print(f"Final Salary (Monthly Basic): Calc={calc_ret['final_monthly_basic']:,} vs CSV 724,511")

print(f"\nWeCare Monthly Pension pre-commutation: Calc={calc_ret['wecare_monthly_pre']:,} vs CSV 362,256")
print(f"WeCare Commuted Lump Sum: Calc={calc_ret['wecare_commuted_lumpsum']:,} vs CSV 15,779,856")
print(f"WeCare Monthly Pension post-commutation: Calc={calc_ret['wecare_monthly_post']:,} vs CSV 242,711")

print(f"\nTotal Monthly Retirement Income: Calc={calc_ret['total_monthly_income']:,} vs CSV 1,436,882")
print(f"Replacement Ratio: Calc={calc_ret['replacement_ratio']}% vs CSV 79.3%")
