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
from pywaffle import Waffle
from urllib.request import urlopen
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle

from highlight_text import fig_text, ax_text
import itertools
import tempfile
import urllib.request
from charts import pie_chart, box_plot


def load_font_from_url(url):
    # Download font file to a temporary location
    tmp_dir = tempfile.gettempdir()
    font_path = os.path.join(tmp_dir, os.path.basename(url))
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(url, font_path)
    return FontProperties(fname=font_path)


outfit_font = load_font_from_url(
    "https://github.com/Outfitio/Outfit-Fonts/raw/main/fonts/ttf/Outfit-Bold.ttf"
)
cabin_font = load_font_from_url(
    "https://github.com/google/fonts/raw/main/ofl/cabin/Cabin%5Bwdth,wght%5D.ttf"
)

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["http://localhost:5173"],
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


# @app.post("/display_images")
# async def display_images(filename: str):
#     try:
#         df = processed_df[filename]
#         print(df.head())
#         plt.figure(figsize=(10, 5))
#         sns.boxplot(x="num_of_unique_IPs_used", y="category", data=df)
#         os.makedirs("images", exist_ok=True)
#         image_path = os.path.join("images", "ips_used_boxplot.svg")
#         plt.savefig(image_path, format="svg")
#         plt.close()

#         return {"image_url": "/images/ips_used_boxplot.svg"}

#     except Exception as e:
#         return JSONResponse(content={"error": str(e)})


@app.post("/display_images")
async def display_images(filename: str):
    try:
        df = processed_df[filename]
        pie_image_url = pie_chart(df)
        ip_box_plot_url = box_plot(df)
        print(f"pie_image_url: {pie_image_url}")
        print(f"ip_box_plot_url: {ip_box_plot_url}")

        return {
            "pie_image_url": f"/images/pie_chart.svg",
            "ip_box_plot_url": f"/images/ip_box_plot.svg",
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
