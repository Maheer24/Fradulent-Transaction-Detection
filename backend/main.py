from fastapi import FastAPI, File, UploadFile
import pandas as pd
import dill
from io import StringIO
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import seaborn as sns
import matplotlib.pyplot as plt
from fastapi.staticfiles import StaticFiles
import os
from charts import (
    pie_chart,
    cases_by_location,
    unique_ips_by_category,
    wallet_balance_account_age_bubble_chart,
    deposit_status_pie_chart,
    radar_chart_transaction_profiles,
)


app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

origins = ["http://localhost:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["http://localhost:5174"],
)

# Load the trained model
model_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\model\pipeline1.pkl"

transaction_type_detection_model = dill.load(
    open(
        model_path,
        "rb",
    )
)

# Dictionary to store processed dataframe
processed_df = {}


@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()  # reads file as bytes

        # Check if file is an Excel file
        if file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
            df = pd.read_excel(file.file)
        else:
            csv_string = content.decode("utf-8")  # converts bytes into a string
            df = pd.read_csv(
                StringIO(
                    csv_string
                )  # StringIO(csv_string) -> converts string to an in memory (data is stored in RAM) file like object
            )

        # Check if required columns are present
        required_columns = [
            "location",
            "num_of_unique_IPs_used",
            "login_count",
            "num_of_frequent_operations",
            "c2c_place_order_count",
            "c2c_release_order_count",
            "gift_card_created_amount",
            "gift_card_redeemed_amount",
            "amount",
            "wallet_balance",
            "wallet_free_balance",
            "wallet_locked_balance",
            "deposit_status",
            "transaction_time",
            "prev_transaction_time",
            "account_age_days",
        ]

        if not all(col in df.columns for col in required_columns):
            return JSONResponse(
                content={"error": "Required columns missing in uploaded CSV file"},
                status_code=400,
            )

        # Covert date columns to datetime format
        df["transaction_time"] = pd.to_datetime(df["transaction_time"])
        df["prev_transaction_time"] = pd.to_datetime(df["prev_transaction_time"])

        # use the required features only (in case other columns are present)
        input_df = df[required_columns]

        # Map predictions to labels
        prediction_labels = {0: "Anomalous", 1: "Fraudulent", 2: "Normal"}

        df["status"] = transaction_type_detection_model.predict(input_df)
        df["status"] = df["status"].map(prediction_labels)

        # Covert date columns to strings as JSON does not support the datetime data type
        df["transaction_time"] = df["transaction_time"].astype(str)
        df["prev_transaction_time"] = df["prev_transaction_time"].astype(str)

        # print(df.head())

        # processed_df["transaction.csv"] = df
        processed_df[file.filename] = df

        return JSONResponse(content=df.to_dict(orient="records"))

    except UnicodeDecodeError:
        return JSONResponse(
            content={"error": "Upload an Excel or CSV file"}, status_code=400
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/download_csv/")
async def download_csv(filename: str):
    try:
        if filename not in processed_df:
            return JSONResponse(
                content={"error": "No processed file found with this name"},
                status_code=400,
            )

        #  processed_df = {
        #      "transactions.csv": <Pandas DataFrame>,
        #  }
        df = processed_df[filename]

        # in memory text buffer (acts as a file) to temporary store the dataframe before sending to user
        output = StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename= {filename}_predicted.csv"
            },
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.post("/display_images")
async def display_images(filename: str):
    try:
        df = processed_df[filename]

        pie_chart(df)
        cases_by_location(df)
        unique_ips_by_category(df)
        wallet_balance_account_age_bubble_chart(df)
        deposit_status_pie_chart(df)
        radar_chart_transaction_profiles(df)

        return {
            "pie_image_url": f"/images/pie_chart.svg",
            "location_bar_chart_url": f"/images/location_bar_chart.svg",
            "unique_ips_by_category_url": f"/images/unique_ip_bar_chart.svg",
            "wallet_balance_account_age_bubble_chart_url": f"/images/wallet_bal_acc_age_bubble_chart.svg",
            "deposit_status_pie_chart_url": f"/images/deposit_status_pie_chart.svg",
            "radar_chart_transaction_profiles_url": f"/images/radar_chart_transaction_profiles.svg",
        }

        # return {
        #     "pie_image_url": f"/images/{pie_image_url}",
        #     "ip_box_plot_url": f"/images/{ip_box_plot_url}",
        # }

        # df = processed_df[filename]
        # pie_chart(df)

        # return {"image_url": "/images/pie_chart.svg"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
