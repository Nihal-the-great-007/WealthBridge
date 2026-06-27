import sys
import os

sys.path.append(os.path.abspath("api"))
import index

print("Testing WeCare Actuarial calculations inside modified api/index.py...")
data = index._get_base_data()
ret = data["retirement"]
house = data["housing"]

print("\n--- RESULTS ---")
print(f"Total Investable Corpus: {ret['total_corpus']:,} (Expected: 361,961,624)")
print(f"Total Monthly Income: {ret['total_monthly_income']:,} (Expected: 1,436,882)")
print(f"Replacement Ratio: {ret['replacement_ratio']}% (Expected: 79.3%)")

print("\n--- HOUSING RESULTS ---")
print(f"House Price: {house['house_price']:,}")
print(f"Down Payment: {house['down_payment_val']:,} ({house['down_payment_pct']*100}%)")
print(f"Loan Amount: {house['loan_amount']:,}")
print(f"EMI: {house['monthly_emi']:,}")
print(f"Safe EMI Limit: {house['safe_emi_limit']:,}")
print(f"Is Affordable: {house['is_affordable']}")
print(f"Max Affordable House Price: {house['max_affordable_house_price']:,}")

assert abs(ret['total_corpus'] - 361961624) < 10, "Corpus mismatch!"
assert abs(ret['total_monthly_income'] - 1436882) < 10, "Monthly income mismatch!"
print("\nAll assertions passed! Calculation matches CSV file exactly!")
