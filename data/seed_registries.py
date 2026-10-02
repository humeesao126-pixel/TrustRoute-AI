import sqlite3
import os

os.makedirs("data", exist_ok=True)
db_path = os.path.join("data", "registries.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Pakistan BEOE Registry Snapshot (OEPs)
cursor.execute("""
CREATE TABLE IF NOT EXISTS beoe_oep (
    license_no TEXT PRIMARY KEY,
    agency_name TEXT,
    city TEXT,
    status TEXT,
    expiry_date TEXT
)
""")

# 2. Germany Handelsregister Snapshot
cursor.execute("""
CREATE TABLE IF NOT EXISTS handelsregister (
    company_name TEXT,
    register_id TEXT PRIMARY KEY,
    legal_form TEXT,
    court_city TEXT,
    status TEXT
)
""")

# Seed mock records
oep_data = [
    ("1234/LHR", "Al-Saqib Overseas Promoters", "Lahore", "ACTIVE", "2027-12-31"),
    ("4521/RWP", "Rawal Global Consultants", "Rawalpindi", "SUSPENDED", "2025-05-15"),
    ("9812/KHI", "Indus Valley Manpower", "Karachi", "ACTIVE", "2026-11-20"),
]

hr_data = [
    ("Siemens Healthineers GmbH", "HRB 21400", "GmbH", "Munich", "ACTIVE"),
    ("Bavaria Cloud Solutions GmbH", "HRB 94821 B", "GmbH", "Berlin", "ACTIVE"),
    ("Apex Logistik UG", "HRB 10293", "UG", "Frankfurt", "LIQUIDATION"),
]

cursor.executemany("INSERT OR REPLACE INTO beoe_oep VALUES (?, ?, ?, ?, ?)", oep_data)
cursor.executemany("INSERT OR REPLACE INTO handelsregister VALUES (?, ?, ?, ?, ?)", hr_data)

conn.commit()
conn.close()
print("Registries seeded successfully in data/registries.db")