import urllib.request
import json
import time

print("Waiting 3 seconds for server to settle...")
time.sleep(3)

# 1. Test /api/data (GET)
print("Testing GET /api/data...")
try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/data") as response:
        body = response.read().decode("utf-8")
        data = json.loads(body)
        print("Success! /api/data returned status 200.")
        print(f"Investable Corpus: {data['retirement']['total_corpus']:,}")
        print(f"Monthly Retirement Income: {data['retirement']['total_monthly_income']:,}")
        print(f"Replacement Ratio: {data['retirement']['replacement_ratio']}%")
        print(f"Housing Price: {data['housing']['house_price']:,}")
        print(f"Housing EMI: {data['housing']['monthly_emi']:,}")
        print(f"Housing Affordable: {data['housing']['is_affordable']}")
        
        # Verify correctness
        assert abs(data['retirement']['total_corpus'] - 361961624) < 10, "Corpus mismatch!"
        assert abs(data['retirement']['total_monthly_income'] - 1436882) < 10, "Income mismatch!"
except Exception as e:
    print(f"Error testing /api/data: {e}")
    sys.exit(1)

# 2. Test /api/calculate (POST)
print("\nTesting POST /api/calculate with housing override...")
# Let's override house price to ₹5,000,000 (which should make it safe / affordable)
payload = {
    "current_age": 28,
    "retirement_age": 60,
    "starting_ctc": 2_000_000,
    "salary_growth": 0.08,
    "inflation": 0.06,
    "post_ret_inflation": 0.05,
    "basic_pct": 0.40,
    "income_tax_rate": 0.20,
    "epf_employee_rate": 0.12,
    "epf_employer_rate": 0.12,
    "epf_return": 0.0815,
    "nps_employee_pct": 0.05,
    "nps_employer_pct": 0.10,
    "nps_blended_return": 0.1075,
    "nps_annuity_pct": 0.40,
    "nps_annuity_rate": 0.055,
    "elss_monthly_sip": 10000,
    "elss_stepup": 0.10,
    "elss_net_return": 0.12,
    "elss_swr": 0.04,
    "wecare_employee_pct": 0.10,
    "wecare_pension_pct": 0.50,
    "wecare_commutation_pct": 0.33,
    "commutation_factor": 11.0,
    "life_expectancy": 85,
    "housing_house_price": 5_000_000, # override to 50 Lakhs
    "housing_down_payment_pct": 0.20,
    "housing_loan_rate": 0.075,
    "housing_loan_tenure": 20,
    "housing_safe_emi_pct": 0.35
}

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/calculate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        body = response.read().decode("utf-8")
        data = json.loads(body)
        print("Success! /api/calculate returned status 200.")
        print(f"Recalculated EMI: {data['housing']['monthly_emi']:,}")
        print(f"Recalculated Safe Limit: {data['housing']['safe_emi_limit']:,}")
        print(f"Recalculated Affordable: {data['housing']['is_affordable']}")
        assert data['housing']['is_affordable'] is True, "Expected house of 50L to be affordable!"
except Exception as e:
    print(f"Error testing /api/calculate: {e}")
    sys.exit(1)

print("\nAll endpoints tested and validated successfully!")
