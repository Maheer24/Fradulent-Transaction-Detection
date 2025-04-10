import dill
import pandas as pd
import numpy as np

pipeline = dill.load(
    open(
        r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\model\pipeline1.pkl",
        "rb",
    )
)


def predict_transaction_type(user_input):
    user_input["deposit_status"] = str(
        user_input["deposit_status"]
    )  # Ensure deposit_status is a string

    # Convert dictionary into a DataFrame properly
    input_data = pd.DataFrame(user_input)

    # Ensure correct data types
    data_types = {
        "location": "str",
        "num_of_unique_IPs_used": "int64",
        "login_count": "int64",
        "num_of_frequent_operations": "int64",
        "c2c_place_order_count": "int64",
        "c2c_release_order_count": "int64",
        "gift_card_created_amount": "float64",
        "gift_card_redeemed_amount": "float64",
        "amount": "float64",
        "wallet_balance": "float64",
        "wallet_free_balance": "float64",
        "wallet_locked_balance": "float64",
        "account_age_days": "int64",
    }

    # Apply type conversion with error handling
    for col, dtype in data_types.items():
        try:
            input_data[col] = input_data[col].astype(dtype)
        except ValueError as e:
            print(f"Type conversion error in column '{col}': {e}")

    # Ensure date-time columns are properly converted
    input_data["transaction_time"] = pd.to_datetime(
        input_data["transaction_time"], errors="coerce"
    )
    input_data["prev_transaction_time"] = pd.to_datetime(
        input_data["prev_transaction_time"], errors="coerce"
    )

    print("\nBefore pipeline transformation:\n", input_data)

    # Make sure input is passed as DataFrame, not a list
    if not isinstance(input_data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame")

    # Ensure pipeline compatibility
    prediction = pipeline.predict(input_data)

    return prediction[0] if isinstance(prediction, list) else prediction


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

pred = predict_transaction_type(custom_input)
print(pred)
