import os
import io
import json
import pandas as pd
from azure.storage.blob import BlobServiceClient

CONNECT_STR = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey="
    "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

CONTAINER = "datasets"
BLOB_NAME = "All_Diets.csv"

OUT_DIR = "simulated_nosql"
OUT_FILE = os.path.join(OUT_DIR, "results.json")

def process_nutritional_data_from_azurite():
    os.makedirs(OUT_DIR, exist_ok=True)

    blob_service = BlobServiceClient.from_connection_string(CONNECT_STR)
    container_client = blob_service.get_container_client(CONTAINER)
    blob_client = container_client.get_blob_client(BLOB_NAME)

    # Download blob content
    data = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(data))

    macro_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]
    for c in macro_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df[macro_cols] = df[macro_cols].fillna(df[macro_cols].mean(numeric_only=True))

    avg_macros = df.groupby("Diet_type")[macro_cols].mean().reset_index()

    result = avg_macros.to_dict(orient="records")

    with open(OUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    return f"Processed blob and stored results in {OUT_FILE}"

if __name__ == "__main__":
    print(process_nutritional_data_from_azurite())

