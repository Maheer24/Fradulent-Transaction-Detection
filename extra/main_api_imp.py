import requests
import pandas as pd

url = "http://127.0.0.1:8000/upload_csv"

#file_path = r"C:\Users\HP\Desktop\Python\Data_Science_Projects\fradulent-transaction-detection\api_test_data.csv"
file_path = r"C:\Users\HP\Documents\api_test_data.xlsx"

with open(file_path, "rb") as file:
    response = requests.post(url, files={"file": file})

print(f"Status code: {response.status_code}")
print(f"Response JSON: {response.json()}")


