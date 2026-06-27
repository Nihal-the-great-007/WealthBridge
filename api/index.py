"""
WeCare Retirement Model | Track 1: Wealth & Pensions
Author: WeCare Team
"""
from __future__ import annotations

import math
import logging
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# -- Logging Setup -------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("wealthbridge")

# -- Path Resolution -----------------------------------------------------------
# Vercel: __file__ = /var/task/api/index.py     parent.parent = /var/task (project root)
# Local:  resolves to project root (one level above /api/)
BASE_DIR = Path(__file__).resolve().parent.parent

_CSV_NAMES = {
    "assumptions": "WeCare_Financial_Model-1(ASSUMPTIONS).csv",
    "salary":      "WeCare_Financial_Model-1(SALARY_PROJ).csv",
    "corpus":      "WeCare_Financial_Model-1(CORPUS_BUILD).csv",
    "retirement":  "WeCare_Financial_Model-1(RETIREMENT).csv",
}


def _csv_path(key: str) -> Path:
    """Resolve a CSV file path relative to project root with fallback to CWD."""
    name = _CSV_NAMES[key]
    for candidate in (BASE_DIR / name, Path.cwd() / name, Path(name)):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Cannot locate '{name}'. Searched: {BASE_DIR}, {Path.cwd()}"
    )


# -- Number Parsing Utility ----------------------------------------------------
def _num(val: Any) -> Optional[float]:
    """
    Parse Indian-formatted numbers robustly.
    Handles: commas, Rupee prefix, % suffix, 'nan', dash placeholders.
    """
    if val is None:
        return None
    s = str(val).strip()
    if s in ("", "-", "N/A", "nan", "None", "NaN", "#REF!", "#VALUE!"):
        return None
    s = s.replace(",", "").replace("\u20b9", "").replace("%", "").strip()
    try:
        f = float(s)
        return None if math.isnan(f) or math.isinf(f) else f
    except (ValueError, OverflowError):
        return None


# -- ASSUMPTIONS CSV Loader ----------------------------------------------------
def _search_df(df: pd.DataFrame, keyword: str, col: int = 1, default: float = 0.0) -> float:
    """
    Scan all rows for 'keyword' in column 0 (case-insensitive partial match).
    Returns the numeric value from column 'col' in that row, or 'default'.
    """
    kw = keyword.lower()
    for _, row in df.iterrows():
        label = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        if kw in label.lower():
            if len(row) > col and pd.notna(row.iloc[col]):
                v = _num(str(row.iloc[col]))
                if v is not None:
                    return v
    return default


def load_assumptions() -> dict:
    """
    Parse ASSUMPTIONS CSV into a structured parameter dictionary.
    Values stored as percentages in CSV (e.g. 8.15 for 8.15%) are
    normalised to decimals (0.0815) for all rate/ratio fields.
    """
    df = pd.read_csv(_csv_path("assumptions"), header=None, dtype=str, on_bad_lines="skip", encoding="latin1")

    raw: dict[str, float] = {
        "current_age":            _search_df(df, "Current Age (years)",                             default=28),
        "retirement_age":         _search_df(df, "Normal Retirement Age (years)",                   default=60),
        "starting_ctc":           _search_df(df, "Starting Annual CTC",                             default=2_000_000),
        "basic_pct":              _search_df(df, "Basic Salary as % of CTC",                        default=40),
        "expense_pct":            _search_df(df, "Current Monthly Expenses as % of Net Salary",     default=50),
        "salary_growth":          _search_df(df, "Annual Salary Growth Rate",                       default=8),
        "inflation":              _search_df(df, "Inflation Rate (CPI)",                            default=6),
        "post_ret_inflation":     _search_df(df, "Post-Retirement Inflation",                       default=5),
        "epf_employee_rate":      _search_df(df, "EPF Employee Contribution Rate",                  default=12),
        "epf_employer_rate":      _search_df(df, "EPF Employer Contribution Rate",                  default=12),
        "epf_return":             _search_df(df, "EPF Interest Rate",                               default=8.15),
        "vpf_rate":               _search_df(df, "Voluntary Provident Fund (VPF) Additional",       default=0),
        "nps_employee_pct":       _search_df(df, "NPS Employee Voluntary Contribution",             default=5),
        "nps_employer_pct":       _search_df(df, "NPS Employer Contribution (% of basic)",          default=10),
        "nps_equity_alloc":       _search_df(df, "NPS Equity Allocation",                           default=75),
        "nps_equity_return":      _search_df(df, "NPS Equity Fund Expected Return",                 default=12),
        "nps_debt_return":        _search_df(df, "NPS Debt Fund Expected Return",                   default=7),
        "nps_blended_return":     _search_df(df, "NPS Blended Return",                              default=10.75),
        "nps_annuity_pct":        _search_df(df, "NPS Annuity Compulsion",                          default=40),
        "nps_annuity_rate":       _search_df(df, "NPS Annuity Purchase Rate",                       default=5.5),
        "elss_monthly_sip":       _search_df(df, "Monthly ELSS / Equity MF SIP",                   default=10_000),
        "elss_stepup":            _search_df(df, "ELSS / Equity MF SIP Annual Step-Up Rate",        default=10),
        "elss_gross_return":      _search_df(df, "ELSS / Equity MF Expected Return (gross)",        default=13),
        "elss_expense_ratio":     _search_df(df, "ELSS / MF Expense Ratio",                        default=1),
        "elss_swr":               _search_df(df, "ELSS Safe Withdrawal Rate",                       default=4),
        "wecare_employee_pct":    _search_df(df, "WeCare Employee Contribution (% of basic/month)", default=10),
        "wecare_return":          _search_df(df, "WeCare Fund Return Rate",                          default=8.75),
        "wecare_pension_pct":     _search_df(df, "WeCare Employer Guaranteed Pension",              default=50),
        "wecare_commutation_pct": _search_df(df, "WeCare Commutation %",                            default=33),
        "commutation_factor":     _search_df(df, "Commutation Factor (lump sum per",                default=11.0),
        "income_tax_rate":        _search_df(df, "Effective Income Tax Rate on Gross Salary",       default=20),
        "housing_house_price":     _search_df(df, "Target House Purchase Price",                     default=15_000_000),
        "housing_down_payment_pct":_search_df(df, "Down Payment as % of House Price",               default=20),
        "housing_loan_rate":       _search_df(df, "Home Loan Interest Rate (p.a.)",                  default=7.5),
        "housing_loan_tenure":     _search_df(df, "Home Loan Tenure (years)",                        default=20),
        "housing_safe_emi_pct":    _search_df(df, "Safe EMI-to-Net-Take-Home Threshold",             default=35),
    }

    # Normalise percentage fields: if stored as >= 1 they are in %-points, not decimals.
    # e.g.: 8.15%     8.15 (parsed)     / 100     0.0815
    #        1.0%     1.0  (parsed)     / 100     0.01   (expense ratio threshold: >= 1.0)
    pct_keys = [
        "basic_pct", "expense_pct", "salary_growth", "inflation", "post_ret_inflation",
        "epf_employee_rate", "epf_employer_rate", "epf_return", "vpf_rate",
        "nps_employee_pct", "nps_employer_pct", "nps_equity_alloc",
        "nps_equity_return", "nps_debt_return", "nps_blended_return",
        "nps_annuity_pct", "nps_annuity_rate",
        "elss_stepup", "elss_gross_return", "elss_expense_ratio", "elss_swr",
        "wecare_employee_pct", "wecare_pension_pct",
        "wecare_commutation_pct", "wecare_return", "income_tax_rate",
        "housing_down_payment_pct", "housing_loan_rate", "housing_safe_emi_pct",
    ]
    for k in pct_keys:
        if raw[k] >= 1.0:  # >= 1.0 catches both 1.0% (=1.0) and 8.15% (=8.15)
            raw[k] = raw[k] / 100.0

    # Derived computed fields
    raw["elss_net_return"]      = raw["elss_gross_return"] - raw["elss_expense_ratio"]
    raw["accumulation_years"]   = int(raw["retirement_age"] - raw["current_age"])

    logger.info("Assumptions loaded: age %s   %s | CTC    %.0f | EPF %.2f%% | NPS %.2f%% | ELSS %.2f%%",
                raw["current_age"], raw["retirement_age"], raw["starting_ctc"],
                raw["epf_return"] * 100, raw["nps_blended_return"] * 100, raw["elss_net_return"] * 100)
    return raw


# -- Core Actuarial Calculation Engine ----------------------------------------
def compute_projections(p: dict) -> dict:
    """
    Year-by-year actuarial projection engine.

    Uses Python ``decimal.Decimal`` for all intermediate arithmetic to
    eliminate floating-point accumulation errors across 32 compounding steps.

    Returns
    -------
    dict with keys:
        salary_proj  : list[dict]  - per-year salary & contribution breakdowns
        corpus_build : list[dict]  - per-year EPF/NPS/ELSS/PPF corpus values
        retirement   : dict        - retirement income, replacement ratio, lump sums
    """
    D    = Decimal
    ZERO = D("0")
    R2   = D("0.01")   # 2 d.p.
    R0   = D("1")      # integer rounding

    def to_d(v) -> Decimal:
        return D(str(v))

    def r0(d: Decimal) -> float:
        """Round to nearest rupee and return as float."""
        return float(d.quantize(R0, rounding=ROUND_HALF_UP))

    def r2(d: Decimal) -> float:
        """Round to 2 decimal places and return as float."""
        return float(d.quantize(R2, rounding=ROUND_HALF_UP))

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
    wc_ret         = to_d(p.get("wecare_return", 0.0875))  # 8.75% plan-fixed, now parameterisable
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

        # -- Salary computation -----------------------------------------------
        growth_factor = (D("1") + salary_growth) ** (yr - 1)
        ctc           = starting_ctc * growth_factor
        basic_pa      = ctc * basic_pct
        basic_pm      = basic_pa / D("12")

        # -- EPF -------------------------------------------------------------
        epf_emp_pm  = basic_pm * epf_emp_r
        epf_empr_pm = basic_pm * epf_empr_r
        epf_annual  = (epf_emp_pm + epf_empr_pm) * D("24") # doubled in spreadsheet

        # -- NPS -------------------------------------------------------------
        nps_emp_pm  = basic_pm * nps_emp_r
        nps_empr_pm = basic_pm * nps_empr_r
        nps_annual  = (nps_emp_pm + nps_empr_pm) * D("12")

        # -- WeCare DB (employee contribution only; employer bears pension) ---
        wc_pm      = basic_pm * wc_emp_r
        wc_annual  = wc_pm * D("24") # doubled in spreadsheet

        # -- ELSS SIP with annual step-up -------------------------------------
        if yr > 1:
            elss_monthly_cur = elss_monthly_cur * (D("1") + elss_stepup)
        elss_annual = elss_monthly_cur * D("12")

        # -- Corpus end-of-year compounding ------------------------------------
        if yr == 1:
            epf_corpus  = epf_annual  * (D("1") + epf_ret)
            nps_corpus  = nps_annual  * (D("1") + nps_ret)
            elss_corpus = elss_annual * (D("1") + elss_ret)
            wc_cumul    = wc_annual   * (D("1") + wc_ret)   # was hardcoded 1.0875
        else:
            epf_corpus  = epf_corpus  * (D("1") + epf_ret)  + epf_annual
            nps_corpus  = nps_corpus  * (D("1") + nps_ret)  + nps_annual
            elss_corpus = elss_corpus * (D("1") + elss_ret) + elss_annual
            wc_cumul    = wc_cumul    * (D("1") + wc_ret)   + wc_annual   # was hardcoded 1.0875
        total_c     = epf_corpus + nps_corpus + elss_corpus + wc_cumul

        # -- Net Take-Home -----------------------------------------------------
        gross_pm     = ctc / D("12")
        tax_pm       = gross_pm * income_tax
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
    wc_lumpsum       = wc_commuted_ann * comm_factor         #  - 11x = lump sum
    wc_monthly_post  = wc_monthly_pre * (D("1") - wc_comm_pct)  # Remaining recurring

    # Capitalised pre-commutation WeCare corpus equivalent
    wecare_corpus    = wc_annual_pen * comm_factor
    total_c          = epf_c + nps_c + elss_c + wc_cum

    # EPF monthly income via 5.5% p.a. annuity (full corpus annuitised)
    epf_monthly_ann  = epf_c * nps_ann_rate / D("12")

    # NPS split: 40%     annuity, 60%     tax-free lump sum
    nps_lumpsum      = nps_c * (D("1") - nps_ann_pct)
    nps_ann_corpus   = nps_c * nps_ann_pct
    nps_monthly_ann  = nps_ann_corpus * nps_ann_rate / D("12")

    # ELSS 4% Safe Withdrawal Rate     monthly sustainable income
    elss_monthly_swr = elss_c * elss_swr / D("12")

    # Total monthly retirement income (pre-commutation: uses wc_monthly_pre to match the spreadsheet)
    total_monthly    = epf_monthly_ann + nps_monthly_ann + wc_monthly_pre + elss_monthly_swr

    # Replacement ratio vs final gross monthly CTC
    last_sal          = salary_proj[-1]
    final_monthly_ctc = to_d(str(last_sal["annual_ctc"])) / D("12")
    replacement_ratio = r2(total_monthly / final_monthly_ctc * D("100"))

    # Corpus breakdown: invested vs compound returns
    total_epf_inv   = r0(to_d(str(sum(r["epf_annual"]    for r in corpus_build))))
    total_nps_inv   = r0(to_d(str(sum(r["nps_annual"]    for r in corpus_build))))
    total_elss_inv  = r0(to_d(str(sum(r["elss_annual"]   for r in corpus_build))))
    # WeCare: sum actual annual employee contributions (NOT the accumulated corpus)
    total_wecare_inv = r0(to_d(str(sum(r["wecare_annual"] for r in corpus_build))))
    total_invested  = total_epf_inv + total_nps_inv + total_elss_inv + total_wecare_inv
    total_returns   = r0(total_c) - total_invested

    retirement = {
        # Corpus
        "epf_corpus":             r0(epf_c),
        "nps_corpus":             r0(nps_c),
        "elss_corpus":            r0(elss_c),
        "wecare_corpus":          r0(wecare_corpus),     # Capitalised DB pension value
        "wecare_cumul_emp":       r0(wc_cum),            # Employee contribution fund
        "total_corpus":           r0(total_c),
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
        # Invested vs Returns breakdown (actual contributions, not accumulated corpus)
        "total_epf_invested":     total_epf_inv,
        "total_nps_invested":     total_nps_inv,
        "total_elss_invested":    total_elss_inv,
        "total_wecare_invested":  total_wecare_inv,   # ₹2.1474 Cr raw contributions
        "total_invested":         total_invested,
        "total_returns":          total_returns,
    }

    # -- Housing and Home Loan Affordability Analysis -------------------------
    h_price = float(p.get("housing_house_price", 15_000_000))
    h_down_pct = float(p.get("housing_down_payment_pct", 0.20))
    h_rate = float(p.get("housing_loan_rate", 0.075))
    h_tenure = float(p.get("housing_loan_tenure", 20))
    h_safe_pct = float(p.get("housing_safe_emi_pct", 0.35))

    h_down_val = h_price * h_down_pct
    h_loan_amt = h_price - h_down_val

    # Monthly EMI formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    if h_loan_amt > 0 and h_rate > 0 and h_tenure > 0:
        r_m = h_rate / 12.0
        n_m = h_tenure * 12.0
        h_emi = h_loan_amt * r_m * ((1.0 + r_m) ** n_m) / (((1.0 + r_m) ** n_m) - 1.0)
    else:
        h_emi = 0.0

    # Year 1 net take-home (first item in salary_proj)
    y1_takehome = float(salary_proj[0]["net_takehome_pm"]) if salary_proj else 0.0
    h_safe_emi_limit = y1_takehome * h_safe_pct
    h_is_affordable = h_emi <= h_safe_emi_limit

    # Max affordable loan amount based on safe EMI
    if h_rate > 0 and h_tenure > 0:
        r_m = h_rate / 12.0
        n_m = h_tenure * 12.0
        h_max_loan = h_safe_emi_limit * (((1.0 + r_m) ** n_m) - 1.0) / (r_m * ((1.0 + r_m) ** n_m))
    else:
        h_max_loan = 0.0

    h_max_house_price = h_max_loan / (1.0 - h_down_pct) if h_down_pct < 1.0 else h_max_loan

    housing = {
        "house_price":               round(h_price, 0),
        "down_payment_pct":          round(h_down_pct, 4),
        "down_payment_val":          round(h_down_val, 0),
        "loan_amount":               round(h_loan_amt, 0),
        "interest_rate":             round(h_rate, 4),
        "tenure_years":              round(h_tenure, 1),
        "monthly_emi":               round(h_emi, 0),
        "safe_emi_limit":            round(h_safe_emi_limit, 0),
        "is_affordable":             bool(h_is_affordable),
        "max_affordable_loan":       round(h_max_loan, 0),
        "max_affordable_house_price": round(h_max_house_price, 0),
    }

    return {
        "salary_proj":  salary_proj,
        "corpus_build": corpus_build,
        "retirement":   retirement,
        "housing":      housing,
    }


# -- Monte Carlo Stochastic Simulation ----------------------------------------
_MC_ITERATIONS = 2_000
_RNG_SEED_ACC  = 42     # Accumulation phase RNG seed (reproducible)
_RNG_SEED_DEC  = 123    # Decumulation phase RNG seed

# Asset-class annual return standard deviations (  )
_SIGMA = {
    "epf":  0.02,   # Sovereign-guaranteed     very tight dispersion
    "nps":  0.10,   # Blended 75% equity / 25% debt
    "elss": 0.15,   # Pure large-cap equity (Nifty-class)
    "ppf":  0.01,   # Government quarterly-reviewed fixed rate     minimal variance
}


def run_monte_carlo(p: dict, corpus_build: list[dict]) -> dict:
    """
    Execute a 2,000-path Monte Carlo simulation across the full accumulation
    timeline and a subsequent decumulation survival test to age ``life_expectancy``.

    Each simulation draws annual return rates from independent Normal distributions:
        EPF:  N(  =8.15%,   =2%)
        NPS:  N(  =10.75%,   =10%)
        ELSS: N(  =12%,   =15%)
        PPF:  N(  =7.1%,   =1%)

    Returns
    -------
    dict with keys:
        ages               : list[int]   - age labels for x-axis
        p10, p50, p90      : list[float] - percentile wealth curves (   )
        success_probability: float       - % of simulations where corpus > 0 at life_expectancy
        iterations         : int
        life_expectancy    : int
    """
    years           = int(p["retirement_age"] - p["current_age"])
    life_expectancy = int(p.get("life_expectancy", 85))
    retirement_yrs  = max(1, life_expectancy - int(p["retirement_age"]))

    mu_epf  = float(p["epf_return"])
    mu_nps  = float(p["nps_blended_return"])
    mu_elss = float(p["elss_net_return"])

    # Contribution arrays from base-case deterministic projections (shape: [years])
    epf_c_arr  = np.array([r["epf_annual"]  for r in corpus_build], dtype=np.float64)
    nps_c_arr  = np.array([r["nps_annual"]  for r in corpus_build], dtype=np.float64)
    elss_c_arr = np.array([r["elss_annual"] for r in corpus_build], dtype=np.float64)

    rng = np.random.default_rng(seed=_RNG_SEED_ACC)

    # Draw annual returns: shape [_MC_ITERATIONS, years]
    ret_epf  = rng.normal(mu_epf,  _SIGMA["epf"],  (_MC_ITERATIONS, years)).clip(-0.10, 0.20)
    ret_nps  = rng.normal(mu_nps,  _SIGMA["nps"],  (_MC_ITERATIONS, years)).clip(-0.25, 0.40)
    ret_elss = rng.normal(mu_elss, _SIGMA["elss"], (_MC_ITERATIONS, years)).clip(-0.40, 0.55)

    # -- Accumulation Phase (vectorised) --------------------------------------
    # corpus matrices: shape [_MC_ITERATIONS, years]
    epf_mat  = np.zeros((_MC_ITERATIONS, years), dtype=np.float64)
    nps_mat  = np.zeros((_MC_ITERATIONS, years), dtype=np.float64)
    elss_mat = np.zeros((_MC_ITERATIONS, years), dtype=np.float64)

    for yi in range(years):
        prev_epf  = epf_mat[:, yi - 1]  if yi > 0 else np.zeros(_MC_ITERATIONS)
        prev_nps  = nps_mat[:, yi - 1]  if yi > 0 else np.zeros(_MC_ITERATIONS)
        prev_elss = elss_mat[:, yi - 1] if yi > 0 else np.zeros(_MC_ITERATIONS)

        if yi == 0:
            epf_mat[:, yi]  = epf_c_arr[yi] * (1.0 + ret_epf[:, yi])
            nps_mat[:, yi]  = nps_c_arr[yi] * (1.0 + ret_nps[:, yi])
            elss_mat[:, yi] = elss_c_arr[yi] * (1.0 + ret_elss[:, yi])
        else:
            epf_mat[:, yi]  = prev_epf  * (1.0 + ret_epf[:, yi])  + epf_c_arr[yi]
            nps_mat[:, yi]  = prev_nps  * (1.0 + ret_nps[:, yi])  + nps_c_arr[yi]
            elss_mat[:, yi] = prev_elss * (1.0 + ret_elss[:, yi]) + elss_c_arr[yi]

    wc_cumul_arr = np.array([r["wecare_cumul"] for r in corpus_build], dtype=np.float64)
    total_mat = epf_mat + nps_mat + elss_mat + wc_cumul_arr  # [_MC_ITERATIONS, years]

    # Percentile curves per accumulation year
    p10 = np.percentile(total_mat, 10, axis=0)
    p50 = np.percentile(total_mat, 50, axis=0)
    p90 = np.percentile(total_mat, 90, axis=0)

    # -- Decumulation / Corpus Survival Test -----------------------------------
    # At retirement: total investable corpus = EPF + NPS + ELSS + PPF
    # Monthly retirement income (target drawdown):
    #   EPF annuity + NPS annuity + WeCare DB pension + ELSS SWR
    # The corpus grows at a post-retirement blended rate while being depleted
    # by inflation-adjusted monthly withdrawals.
    # Success criterion: total corpus > 0 at month (life_expectancy     retirement_age)  - 12

    nps_ann_pct  = float(p["nps_annuity_pct"])
    nps_ann_rate = float(p["nps_annuity_rate"])
    elss_swr_r   = float(p["elss_swr"])
    wc_pen_pct   = float(p["wecare_pension_pct"])
    wc_comm_pct  = float(p["wecare_commutation_pct"])
    post_inf     = float(p.get("post_ret_inflation", 0.05))
    comm_factor  = float(p.get("commutation_factor", 11.0))

    # Final salary (deterministic)
    final_sal_annual = float(p["starting_ctc"]) * (1.0 + float(p["salary_growth"])) ** (years - 1)
    final_basic_pm   = final_sal_annual * float(p["basic_pct"]) / 12.0

    # WeCare DB pre-commutation monthly pension (deterministic employer obligation)
    wc_monthly_pre   = final_basic_pm * wc_pen_pct
    wecare_corpus    = wc_monthly_pre * 12.0 * comm_factor

    # Per-simulation corpus at retirement (excludes WeCare corpus)
    fin_epf  = epf_mat[:, -1]
    fin_nps  = nps_mat[:, -1]
    fin_elss = elss_mat[:, -1]
    total_at_ret = fin_epf + fin_nps + fin_elss  # shape [_MC_ITERATIONS]

    # Per-simulation monthly income at retirement (pre-commuted)
    epf_ann_pm  = fin_epf  * nps_ann_rate / 12.0
    nps_ann_pm  = fin_nps  * nps_ann_pct * nps_ann_rate / 12.0
    elss_swr_pm = fin_elss * elss_swr_r / 12.0
    monthly_inc = epf_ann_pm + nps_ann_pm + wc_monthly_pre + elss_swr_pm  # [_MC_ITERATIONS]

    # Personal assets withdrawal amount (WeCare DB pension is paid separately by employer)
    personal_draw_pm = epf_ann_pm + nps_ann_pm + elss_swr_pm              # [_MC_ITERATIONS]

    # Post-retirement blended return distribution
    # Conservative:   =8% (glide path equity reduction),   =8%
    MU_POST  = 0.08
    SIG_POST = 0.08
    rng2 = np.random.default_rng(seed=_RNG_SEED_DEC)
    ret_months   = retirement_yrs * 12
    # Monthly return draws: shape [_MC_ITERATIONS, ret_months]
    ret_post = rng2.normal(MU_POST / 12.0, SIG_POST / (12.0 ** 0.5),
                           (_MC_ITERATIONS, ret_months)).clip(-0.04, 0.07)

    # Vectorised decumulation loop
    corpus_dec = total_at_ret.copy()  # [_MC_ITERATIONS]

    for mo in range(ret_months):
        # Inflation-escalated withdrawal (post-retirement inflation compounds annually)
        infl_factor = (1.0 + post_inf) ** (mo / 12.0)
        draw        = personal_draw_pm * infl_factor            # [_MC_ITERATIONS]
        corpus_dec  = corpus_dec * (1.0 + ret_post[:, mo]) - draw
        corpus_dec  = np.maximum(corpus_dec, 0.0)         # Floor at zero

    success_count = int(np.sum(corpus_dec > 0.0))
    success_prob  = round(success_count / _MC_ITERATIONS * 100.0, 2)

    ages = [int(p["current_age"]) + yr for yr in range(years)]

    logger.info("Monte Carlo complete: %d iters | success=%.1f%% | p50 final=   %.0f Cr",
                _MC_ITERATIONS, success_prob, p50[-1] / 1e7)

    return {
        "ages":                ages,
        "p10":                 [round(float(v), 0) for v in p10],
        "p50":                 [round(float(v), 0) for v in p50],
        "p90":                 [round(float(v), 0) for v in p90],
        "success_probability": success_prob,
        "iterations":          _MC_ITERATIONS,
        "life_expectancy":     life_expectancy,
    }


# -- Pydantic Request Schema ---------------------------------------------------
class CalcParams(BaseModel):
    """User-override parameters for POST /api/calculate."""
    current_age:            float = Field(28,        ge=18,   le=60,  description="Current age in years")
    retirement_age:         float = Field(60,        ge=40,   le=70,  description="Target retirement age")
    starting_ctc:           float = Field(2_000_000, ge=0,            description="Starting annual CTC (   )")
    salary_growth:          float = Field(0.08,      ge=0.0,  le=0.25,description="Annual salary growth rate (decimal)")
    inflation:              float = Field(0.06,      ge=0.0,  le=0.15,description="CPI inflation (decimal)")
    post_ret_inflation:     float = Field(0.05,      ge=0.0,  le=0.12,description="Post-retirement inflation (decimal)")
    basic_pct:              float = Field(0.40,      ge=0.30, le=0.60,description="Basic salary as fraction of CTC")
    income_tax_rate:        float = Field(0.20,      ge=0.0,  le=0.40,description="Effective income tax rate (decimal)")
    epf_employee_rate:      float = Field(0.12,      ge=0.0,  le=0.20)
    epf_employer_rate:      float = Field(0.12,      ge=0.0,  le=0.20)
    epf_return:             float = Field(0.0815,    ge=0.0,  le=0.15,description="EPF annual return rate (decimal)")
    nps_employee_pct:       float = Field(0.05,      ge=0.0,  le=0.20,description="NPS employee contribution as % of basic")
    nps_employer_pct:       float = Field(0.10,      ge=0.0,  le=0.20,description="NPS employer contribution as % of basic")
    nps_blended_return:     float = Field(0.1075,    ge=0.0,  le=0.25,description="NPS blended equity+debt return (decimal)")
    nps_annuity_pct:        float = Field(0.40,      ge=0.40, le=1.0, description="Fraction of NPS corpus to annuitise (min 40%)")
    nps_annuity_rate:       float = Field(0.055,     ge=0.0,  le=0.12,description="NPS annuity purchase rate p.a.")
    elss_monthly_sip:       float = Field(10_000,    ge=0,            description="Monthly ELSS SIP amount (   )")
    elss_stepup:            float = Field(0.10,      ge=0.0,  le=0.30,description="Annual SIP step-up rate (decimal)")
    elss_net_return:        float = Field(0.12,      ge=0.0,  le=0.25,description="ELSS net return after expenses (decimal)")
    elss_swr:               float = Field(0.04,      ge=0.02, le=0.08,description="Safe Withdrawal Rate (decimal)")
    wecare_employee_pct:    float = Field(0.10,      description="WeCare employee contribution as % of basic (plan-fixed)")
    wecare_return:          float = Field(0.0875,    ge=0.0, le=0.20, description="WeCare employee fund return rate (plan-fixed 8.75%)")
    wecare_pension_pct:     float = Field(0.50,      description="WeCare guaranteed pension as % of final avg basic")
    wecare_commutation_pct: float = Field(0.33,      description="Fraction of WeCare pension commuted to lump sum")
    commutation_factor:     float = Field(11.0,      description="Lump sum per    1 of annual pension (actuarial factor)")
    life_expectancy:        float = Field(85,        ge=70,   le=100, description="Target life expectancy for survival test")
    housing_house_price:     float = Field(15_000_000, ge=0)
    housing_down_payment_pct:float = Field(0.20,      ge=0.0,  le=1.0)
    housing_loan_rate:       float = Field(0.075,     ge=0.0,  le=0.25)
    housing_loan_tenure:     float = Field(20,        ge=1,    le=40)
    housing_safe_emi_pct:    float = Field(0.35,      ge=0.0,  le=1.0)


# -- In-Memory Cache -----------------------------------------------------------
_cache: dict | None = None


def _get_base_data() -> dict:
    """Load and cache base-case data on first call (warm start)."""
    global _cache
    if _cache is None:
        logger.info("Initialising base-case computation...")
        base_p       = load_assumptions()
        projections  = compute_projections(base_p)
        mc           = run_monte_carlo(base_p, projections["corpus_build"])
        _cache       = {**projections, "monte_carlo": mc, "params": base_p}
        logger.info("Base-case ready: corpus=   %.2f Cr | success=%.1f%%",
                    projections["retirement"]["total_corpus"] / 1e7,
                    mc["success_probability"])
    return _cache


# -- FastAPI Application -------------------------------------------------------
app = FastAPI(
    title="WealthBridge Retirement Financial Model",
    version="2026.1",
    description=(
        "Track 1: Wealth & Pensions. "
        "High-fidelity retirement corpus projection with Monte Carlo stochastic simulation."
    ),
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# -- Route: Serve Dashboard HTML -----------------------------------------------
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_dashboard():
    """Serve the premium dark-mode analytics dashboard."""
    tmpl = BASE_DIR / "templates" / "index.html"
    if not tmpl.exists():
        raise HTTPException(status_code=404, detail=f"Dashboard template not found at {tmpl}")
    return HTMLResponse(content=tmpl.read_text(encoding="utf-8"))


# -- Route: Serve Background Pattern Image -------------------------------------
@app.get("/background-pattern.jpg", include_in_schema=False)
async def get_background_pattern():
    """Serve the bright-mode background pattern image."""
    img_path = BASE_DIR / "templates" / "background-pattern.jpg"
    if not img_path.exists():
        raise HTTPException(status_code=404, detail="Background pattern image not found")
    return FileResponse(img_path)


# -- Route: Serve Splash Screen Background Pattern -----------------------------
@app.get("/guilloche-wavy-vector-background-2B68X8C.jpg", include_in_schema=False)
async def get_splash_pattern():
    """Serve the splash screen background pattern image."""
    img_path = BASE_DIR / "templates" / "guilloche-wavy-vector-background-2B68X8C.jpg"
    if not img_path.exists():
        raise HTTPException(status_code=404, detail="Splash background pattern image not found")
    return FileResponse(img_path)



# -- Route: Favicon .ico -------------------------------------------------------
@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    """Serve browser favicon.ico (multi-size: 16/32/48)."""
    p = BASE_DIR / "templates" / "favicon.ico"
    if not p.exists():
        raise HTTPException(status_code=404, detail="favicon.ico not found")
    return FileResponse(p, media_type="image/x-icon")


# -- Route: SVG Logo -----------------------------------------------------------
@app.get("/logo.svg", include_in_schema=False)
async def get_logo_svg():
    """Serve the SVG vector logo for browser tab, header, and embeds."""
    p = BASE_DIR / "templates" / "logo.svg"
    if not p.exists():
        raise HTTPException(status_code=404, detail="logo.svg not found")
    return FileResponse(p, media_type="image/svg+xml",
                        headers={"Cache-Control": "public, max-age=86400"})


# -- Route: OG Image -----------------------------------------------------------
@app.get("/og-image.png", include_in_schema=False)
async def get_og_image():
    """Serve the Open Graph social preview image (1200x630)."""
    p = BASE_DIR / "templates" / "og-image.png"
    if not p.exists():
        raise HTTPException(status_code=404, detail="og-image.png not found")
    return FileResponse(p, media_type="image/png",
                        headers={"Cache-Control": "public, max-age=86400"})

# -- Route: PWA Web App Manifest -----------------------------------------------
@app.get("/manifest.json", include_in_schema=False)
async def get_manifest():
    """Serve the PWA web app manifest for mobile install support."""
    manifest_path = BASE_DIR / "templates" / "manifest.json"
    if not manifest_path.exists():
        raise HTTPException(status_code=404, detail="manifest.json not found")
    return FileResponse(manifest_path, media_type="application/manifest+json")


# -- Route: PWA Service Worker -------------------------------------------------
@app.get("/sw.js", include_in_schema=False)
async def get_service_worker():
    """Serve the PWA service worker for offline caching and install."""
    sw_path = BASE_DIR / "templates" / "sw.js"
    if not sw_path.exists():
        raise HTTPException(status_code=404, detail="sw.js not found")
    return FileResponse(sw_path, media_type="application/javascript",
                        headers={"Service-Worker-Allowed": "/"})


# -- Route: PWA Icon 192x192 ---------------------------------------------------
@app.get("/icon-192.png", include_in_schema=False)
async def get_icon_192():
    """Serve PWA icon 192x192."""
    p = BASE_DIR / "templates" / "icon-192.png"
    if not p.exists():
        raise HTTPException(status_code=404, detail="icon-192.png not found")
    return FileResponse(p, media_type="image/png")


# -- Route: PWA Icon 512x512 ---------------------------------------------------
@app.get("/icon-512.png", include_in_schema=False)
async def get_icon_512():
    """Serve PWA icon 512x512."""
    p = BASE_DIR / "templates" / "icon-512.png"
    if not p.exists():
        raise HTTPException(status_code=404, detail="icon-512.png not found")
    return FileResponse(p, media_type="image/png")


# -- Route: Apple Touch Icon ---------------------------------------------------
@app.get("/apple-touch-icon.png", include_in_schema=False)
async def get_apple_touch_icon():
    """Serve Apple touch icon for iOS home screen."""
    p = BASE_DIR / "templates" / "apple-touch-icon.png"
    if not p.exists():
        raise HTTPException(status_code=404, detail="apple-touch-icon.png not found")
    return FileResponse(p, media_type="image/png")


# -- Route: Base-Case Data -----------------------------------------------------
@app.get("/api/data", summary="Get base-case structured data for all charts")
async def get_data():
    """
    Returns all base-case data:
    - salary_proj:  32-year salary & contribution projections
    - corpus_build: 32-year EPF/NPS/ELSS/PPF corpus accumulation
    - retirement:   Final corpus, income streams, replacement ratio
    - monte_carlo:  P10/P50/P90 curves + success probability
    - params:       Active assumption set
    """
    try:
        return JSONResponse(content=_get_base_data())
    except FileNotFoundError as exc:
        logger.error("CSV not found: %s", exc)
        raise HTTPException(status_code=503, detail=f"Data source unavailable: {exc}")
    except Exception as exc:
        logger.exception("Unexpected error loading base data")
        raise HTTPException(status_code=500, detail=str(exc))


# -- Route: Recalculate with User Overrides ------------------------------------
@app.post("/api/calculate", summary="Recalculate projections with custom parameters")
async def calculate(params: CalcParams):
    """
    Accepts a full set of user-defined override parameters, re-runs the
    actuarial engine and 2,000-iteration Monte Carlo, and returns updated
    projection data for all dashboard charts and metrics.
    """
    try:
        base = _get_base_data()
        p    = dict(base["params"])        # Start from loaded base assumptions
        p.update(params.model_dump())      # Override with user inputs
        # Ensure derived field stays consistent
        if "elss_gross_return" in p and "elss_expense_ratio" in p:
            p["elss_net_return"] = p["elss_gross_return"] - p["elss_expense_ratio"]

        projections = compute_projections(p)
        mc          = run_monte_carlo(p, projections["corpus_build"])

        # Serialise params (drop non-serialisable types)
        safe_params = {k: v for k, v in p.items() if isinstance(v, (int, float, str, bool))}

        return JSONResponse(content={
            **projections,
            "monte_carlo": mc,
            "params":      safe_params,
        })
    except Exception as exc:
        logger.exception("Calculation error with overrides")
        raise HTTPException(status_code=422, detail=str(exc))


# -- Route: Health Check -------------------------------------------------------
@app.get("/api/health", summary="Liveness probe")
async def health():
    return {
        "status":  "ok",
        "version": "2026.1",
        "model":   "WealthBridge Retirement Financial Model",
        "engine":  "WealthBridge Retirement Engine",
    }
