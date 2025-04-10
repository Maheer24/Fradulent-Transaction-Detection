from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import json
import numpy as np
import dill


app = FastAPI()


class model_input(BaseModel):
    location: str
    num_of_unique_IPs_used: int
    login_count: int
    num_of_frequent_operations: int
    c2c_place_order_count: int
    c2c_release_order_count: int
    gift_card_created_amount: float
    gift_card_redeemed_amount: float
    amount: float
    wallet_balance: float
    wallet_free_balance: float
    wallet_locked_balance: float
    deposit_status: str
    transaction_time: str
    prev_transaction_time: str
    account_age_days: int


# load the saved model
transaction_type_detection_model = dill.load(
    open(
        r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\model\pipeline1.pkl",
        "rb",
    )
)


@app.post("/transaction_type_prediction")
def transaction_type_pred(input_parameters: model_input):
    input_dictionary = input_parameters.model_dump()
    print(input_dictionary)

    # Convert date time strings to date time format
    input_dictionary["transaction_time"] = pd.to_datetime(
        input_dictionary["transaction_time"]
    )
    input_dictionary["prev_transaction_time"] = pd.to_datetime(
        input_dictionary["prev_transaction_time"]
    )

    # Extract input features
    # location = input_dictionary["location"]
    # num_of_unique_IPs_used = input_dictionary["num_of_unique_IPs_used"]
    # login_count = input_dictionary["login_count"]
    # num_of_frequent_operations = input_dictionary["num_of_frequent_operations"]
    # c2c_place_order_count = input_dictionary["c2c_place_order_count"]
    # c2c_release_order_count = input_dictionary["c2c_release_order_count"]
    # gift_card_created_amount = input_dictionary["gift_card_created_amount"]
    # gift_card_redeemed_amount = input_dictionary["gift_card_redeemed_amount"]
    # amount = input_dictionary["amount"]
    # wallet_balance = input_dictionary["wallet_balance"]
    # wallet_free_balance = input_dictionary["wallet_free_balance"]
    # wallet_locked_balance = input_dictionary["wallet_locked_balance"]
    # deposit_status = input_dictionary["deposit_status"]
    # transaction_time = input_dictionary["transaction_time"]
    # prev_transaction_time = input_dictionary["prev_transaction_time"]
    # account_age_days = input_dictionary["account_age_days"]

    # input_list = [
    #     location,
    #     num_of_unique_IPs_used,
    #     login_count,
    #     num_of_frequent_operations,
    #     c2c_place_order_count,
    #     c2c_release_order_count,
    #     gift_card_created_amount,
    #     gift_card_redeemed_amount,
    #     amount,
    #     wallet_balance,
    #     wallet_free_balance,
    #     wallet_locked_balance,
    #     deposit_status,
    #     transaction_time,
    #     prev_transaction_time,
    #     account_age_days,
    # ]

    # input_array = np.array([input_list])

    # Convert dictionary to DataFrame
    input_df = pd.DataFrame([input_dictionary])

    prediction = transaction_type_detection_model.predict(input_df)
    prediction = int(prediction[0])  # prediction -> [2] , prediction[0] -> 2
    print(f"Prediction: {prediction}")

    # Map prediction to labels
    prediction_labels = {0: "Anomalous", 1: "Fraudulent", 2: "Normal"}
    prediction_label = prediction_labels.get(prediction, "Unknown")

    print(f"Predicted Transaction Type: {prediction_label}")

    # Return as JSON
    return {"Predicted Transaction Type": prediction_label}
