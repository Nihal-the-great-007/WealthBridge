import sys
import pandas as pd
import numpy as np

# Add project root to path so we can import from api.index
sys.path.append(".")

# First, modify the file names in api.index dynamically or mock them
import api.index as index

# Force the new filenames
index._CSV_NAMES = {
    "assumptions": "WeCare_Financial_Model-1(ASSUMPTIONS).csv",
    "salary":      "WeCare_Financial_Model-1(SALARY_PROJ).csv",
    "corpus":      "WeCare_Financial_Model-1(CORPUS_BUILD).csv",
    "retirement":  "WeCare_Financial_Model-1(RETIREMENT).csv",
}

print("Running mock calculations...")
p = index.load_assumptions()
res = index.compute_projections(p)

print("\nAssumptions keys:")
for k, v in p.items():
    print(f"  {k}: {v}")

print("\nRetirement outcomes calculated vs CSV:")
calc_ret = res["retirement"]

# Load CSV retirement outcomes
df_ret = pd.read_csv(index._csv_path("retirement"), header=None, encoding='latin1')
print(df_ret.head(15).to_string().encode('ascii', 'ignore').decode())

# Check some specific values
print("\n--- COMPARISONS ---")
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

print(f"\nTotal Monthly Retirement Income: Calc={calc_ret['total_monthly_income']:,} vs CSV 1,317,338")
print(f"Replacement Ratio: Calc={calc_ret['replacement_ratio']}% vs CSV 72.7%")
