import dill
import pandas as pd
import numpy as np

pipeline = dill.load(
    open(
        r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\model\pipeline1.pkl",
        "rb",
    )
)

# Define a custom input as a dictionary
custom_input = {
    "location": ["Karachi"],
    "deposit_status": ["Completed"],
    "num_of_unique_IPs_used": [3],
    "login_count": [15],
    "num_of_frequent_operations": [7],
    "c2c_place_order_count": [2],
    "c2c_release_order_count": [2],
    "gift_card_created_amount": [0],
    "gift_card_redeemed_amount": [0],
    "amount": [50000],
    "wallet_balance": [70000],
    "wallet_free_balance": [50000],
    "wallet_locked_balance": [20000],
    "account_age_days": [365],
    "transaction_time": ["2025-03-14 10:00:00"],
    "prev_transaction_time": ["2025-03-13 15:30:00"],
}

# Convert to DataFrame
custom_df = pd.DataFrame(custom_input)

# Make a prediction using the trained pipeline
custom_prediction = pipeline.predict(custom_df)

if custom_prediction == 0:
    print("Predicted Category: Anomalous")
elif custom_prediction == 1:
    print("Predicted Category: Fraudulent")
else:
    print("Predicted Category: Normal")
