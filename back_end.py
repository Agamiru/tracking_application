import easypost
import json
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRK_DATA_FILES = os.path.join(BASE_DIR, "app\\tracking_data_files")
db_path = os.path.join(BASE_DIR, "app\\db.sqlite3")

prod_key, test_key = "", ""

# Sets values for prod_key and test_key from database
with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()
    select_command = "SELECT * FROM tracking_api_keys WHERE id=?"
    cur.execute(select_command, (1,))
    for id_, p_key, t_key in cur:
        prod_key, test_key = p_key, t_key


test_tracking_codes = {
    "EZ1000000001": "pre_transit",
    "EZ2000000002": "in_transit",
    "EZ3000000003": "out_for_delivery",
    "EZ4000000004": "delivered",
    "EZ5000000005": "return_to_sender",
    "EZ6000000006": "failure",
    "EZ7000000007": "unknown"
}

# 9505511009360147319966
# 1Z930E980365171206

tracking_code = "1Z930E980365171206"
file_name = tracking_code

# Tracking codes must use appropriate api_key
easypost.api_key = test_key if tracking_code in test_tracking_codes else prod_key

# # Create tracker object
tracker = easypost.Tracker.create(
    tracking_code=tracking_code,
    carrier="UPS"
)

# Write api response to file
with open(f"{TRK_DATA_FILES}\\{file_name}.txt", "w") as text:
    json.dump(obj=tracker.to_dict(), fp=text, indent=3)

print(tracker.status)

print(tracker.carrier_detail["destination_location"])


