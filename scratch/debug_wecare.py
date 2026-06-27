import urllib.request, json

r = urllib.request.urlopen('http://127.0.0.1:8000/api/data')
data = json.loads(r.read())
ret = data['retirement']
cb  = data['corpus_build']

print("=== RETIREMENT KEY WECARE VALUES ===")
print("wecare_corpus      (DB capitalised):", f"{ret['wecare_corpus']:>15,.0f}", " <- should be ~3.43 Cr (pension*11x)")
print("wecare_cumul_emp   (emp fund cumul):", f"{ret['wecare_cumul_emp']:>15,.0f}", " <- should be 6,22,58,019")
print("total_corpus:                       ", f"{ret['total_corpus']:>15,.0f}")
print()
print("=== LAST 5 YEARS CORPUS BUILD ===")
for row in cb[-5:]:
    print(f"  Yr {row['year']} | wc_cumul={row['wecare_cumul']:>12,.0f} | wc_corpus_col={row['wecare_corpus']:>12,.0f}")
print()
print("=== TOTAL INVESTED BREAKDOWN ===")
print("total_invested: ", f"{ret['total_invested']:>15,.0f}")
print("total_epf_inv:  ", f"{ret['total_epf_invested']:>15,.0f}")
print("total_nps_inv:  ", f"{ret['total_nps_invested']:>15,.0f}")
print("total_elss_inv: ", f"{ret['total_elss_invested']:>15,.0f}")
wc_inv = ret['total_invested'] - ret['total_epf_invested'] - ret['total_nps_invested'] - ret['total_elss_invested']
print("wecare_inv (derived):", f"{wc_inv:>12,.0f}")
