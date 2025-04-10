import requests
import json
import numpy as np

url = "http://127.0.0.1:8000/transaction_type_prediction"

# input_data_for_model = {
#     "location": ["Karachi"],
#     "deposit_status": ["Completed"],
#     "num_of_unique_IPs_used": [3],
#     "login_count": [15],
#     "num_of_frequent_operations": [7],
#     "c2c_place_order_count": [2],
#     "c2c_release_order_count": [2],
#     "gift_card_created_amount": [0],
#     "gift_card_redeemed_amount": [0],
#     "amount": [50000],
#     "wallet_balance": [70000],
#     "wallet_free_balance": [50000],
#     "wallet_locked_balance": [20000],
#     "account_age_days": [365],
#     "transaction_time": ["2025-03-14 10:00:00"],
#     "prev_transaction_time": ["2025-03-13 15:30:00"],
# }


input_data_for_model = {
    "location": "Karachi",
    "num_of_unique_IPs_used": 30,
    "login_count": 20,
    "num_of_frequent_operations": 10,
    "c2c_place_order_count": 2,
    "c2c_release_order_count": 2,
    "gift_card_created_amount": 3000,
    "gift_card_redeemed_amount": 10000,
    "amount": 20000,
    "wallet_balance": 2000,
    "wallet_free_balance": 1000,
    "wallet_locked_balance": 4000,
    "deposit_status": "Pending",
    "transaction_time": "2024-02-28 14:27:13",
    "prev_transaction_time": "2024-02-02 08:44:25",
    "account_age_days": 20,
}


response = requests.post(url, json=input_data_for_model)
print(response.status_code)
print(response.json())
