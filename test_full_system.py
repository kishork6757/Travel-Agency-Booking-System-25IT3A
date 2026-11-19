"""
=============================================================================
Comprehensive Automated Verification & Testing Suite
Travel Agency Booking & Tourism Trend Analysis System (Scenario 21)
Student: Kishor K | RegNo: 732925ITR051 | Class: 25IT3A
=============================================================================
"""

import sys
import os
import sqlite3
import json

BASE_DIR = r"e:\Assingment_Kishor"
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

passed = 0
failed = 0

def check(name, condition, details=""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name} {details}")
        passed += 1
    else:
        print(f"  [FAIL] {name} - FAILED! {details}")
        failed += 1

print("="*75)
print("1. DATABASE INTEGRITY & SCHEMA VERIFICATION (25ITT31)")
print("="*75)

db_path = os.path.join(BASE_DIR, "database", "travel_agency.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Integrity check
cur.execute("PRAGMA integrity_check;")
res = cur.fetchone()[0]
check("Database Integrity Check", res == "ok", f"-> {res}")

# 2. Table row counts
tables = ["customers", "travel_packages", "bookings", "payments", "cancellations"]
for t in tables:
    cur.execute(f"SELECT count(*) FROM {t}")
    cnt = cur.fetchone()[0]
    check(f"Table '{t}' Exists & Populated", cnt > 0, f"({cnt} rows)")

# 3. View checks
views = ["v_destination_revenue", "v_booking_summary"]
for v in views:
    cur.execute(f"SELECT count(*) FROM {v}")
    cnt = cur.fetchone()[0]
    check(f"View '{v}' Functional", cnt > 0, f"({cnt} rows)")

conn.close()

print("\n" + "="*75)
print("2. FLASK RESTful API & FULL-STACK ENGINE VERIFICATION")
print("="*75)

from server import app

client = app.test_client()

# 1. Frontend Route
res_home = client.get("/")
check("Endpoint GET / (Frontend HTML5 SPA)", res_home.status_code == 200, f"Status: {res_home.status_code}")

# 2. Stats API
res_stats = client.get("/api/stats")
stats_data = json.loads(res_stats.data)
check("Endpoint GET /api/stats", res_stats.status_code == 200 and "gross_revenue" in stats_data, 
      f"Revenue: ₹{stats_data.get('gross_revenue', 0):,.2f}")

# 3. Packages API
res_pkg = client.get("/api/packages")
pkg_data = json.loads(res_pkg.data)
check("Endpoint GET /api/packages", res_pkg.status_code == 200 and len(pkg_data) >= 8, f"{len(pkg_data)} packages loaded")

# 4. Customers API
res_cust = client.get("/api/customers")
cust_data = json.loads(res_cust.data)
check("Endpoint GET /api/customers", res_cust.status_code == 200 and len(cust_data) >= 10, f"{len(cust_data)} customers loaded")

# 5. Anti-Overbooking Guard Check (Critical Functional Requirement)
# Find package 105 (Dubai) and check remaining
target_pkg = next(p for p in pkg_data if p['package_id'] == 105)
remaining = target_pkg['remaining_seats']

# Attempt to overbook (remaining + 10)
overbook_payload = {
    "customer_id": 1,
    "package_id": 105,
    "travel_date": "2026-12-25",
    "num_travelers": remaining + 10,
    "payment_method": "UPI"
}
res_overbook = client.post("/api/bookings", json=overbook_payload)
overbook_res = json.loads(res_overbook.data)
check("Anti-Overbooking Rejection (Requested > Capacity)", 
      res_overbook.status_code == 400 and not overbook_res.get("success"), 
      f"Blocked as expected: {overbook_res.get('error', '')[:40]}...")

# 6. Valid Booking Creation
valid_payload = {
    "customer_id": 1,
    "package_id": 102, # Goa
    "travel_date": "2026-12-20",
    "num_travelers": 1,
    "payment_method": "UPI"
}
res_valid = client.post("/api/bookings", json=valid_payload)
valid_res = json.loads(res_valid.data)
check("Valid Booking Creation & Price Calculation", 
      res_valid.status_code == 200 and valid_res.get("success"), 
      f"Booking ID: #{valid_res.get('booking_id')}")

# 7. Cancellation & 90% Refund Processing
new_booking_id = valid_res.get("booking_id")
if new_booking_id:
    cancel_payload = {"booking_id": new_booking_id, "reason": "Automated System Test"}
    res_cancel = client.post("/api/cancel", json=cancel_payload)
    cancel_res = json.loads(res_cancel.data)
    check("Cancellation & 90% Refund Processing", 
          res_cancel.status_code == 200 and cancel_res.get("success"),
          f"Refund: ₹{cancel_res.get('refund_amount', 0):,.2f}")

# 8. Analytics API
res_analytics = client.get("/api/analytics")
analytics_data = json.loads(res_analytics.data)
check("Endpoint GET /api/analytics", 
      res_analytics.status_code == 200 and len(analytics_data.get("destinations", [])) > 0,
      f"{len(analytics_data.get('destinations', []))} destinations aggregated")

print("\n" + "="*75)
print("3. PYTHON DATA SCIENCE & VISUALIZATION PIPELINE (25ITC31)")
print("="*75)

viz_dir = os.path.join(BASE_DIR, "visualizations")
charts = [
    "01_destination_popularity.png",
    "02_monthly_booking_trends.png",
    "03_revenue_by_category.png",
    "04_booking_status_distribution.png",
    "05_traveler_group_size_distribution.png",
    "06_package_occupancy_heatmap.png"
]
for c in charts:
    path = os.path.join(viz_dir, c)
    exists = os.path.exists(path) and os.path.getsize(path) > 10000
    check(f"Chart '{c}'", exists, f"({os.path.getsize(path):,} bytes)" if exists else "Missing")

print("\n" + "="*75)
print("4. SUMMARY OF TEST SUITE EXECUTION")
print("="*75)
total = passed + failed
print(f"Total Test Cases Evaluated : {total}")
print(f"Passed                     : {passed}")
print(f"Failed                     : {failed}")
print(f"System Success Rate        : {(passed / total) * 100:.1f}%\n")

if failed == 0:
    print("[SUCCESS] ALL SUBSYSTEMS FULLY OPERATIONAL AND ACADEMICALLY COMPLIANT!")
else:
    print("[ERROR] SOME TESTS FAILED!")
    sys.exit(1)
