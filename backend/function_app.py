import azure.functions as func
import logging
import os
import io
import json
import time
import pandas as pd
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.function_name(name="DietAnalysisAPI")
@app.route(route="DietAnalysisAPI", auth_level=func.AuthLevel.ANONYMOUS)
def DietAnalysisAPI(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.time()

    try:
        connection_string = os.environ["BLOB_CONNECTION_STRING"]
        container_name = os.environ["BLOB_CONTAINER_NAME"]
        blob_name = os.environ["BLOB_FILE_NAME"]

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        blob_data = blob_client.download_blob().readall()
        df = pd.read_csv(io.BytesIO(blob_data))

        df.columns = [col.strip() for col in df.columns]

        rows = int(df.shape[0])
        columns = int(df.shape[1])

        # Bar chart
        first_col = df.columns[0]
        bar_counts = df[first_col].astype(str).value_counts().head(10)

        # Pie chart
        second_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
        pie_counts = df[second_col].astype(str).value_counts().head(6)

        # Line chart
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

        if numeric_cols:
            line_col = numeric_cols[0]
            line_series = df[line_col].dropna().head(20).reset_index(drop=True)
            line_labels = [f"Row {i+1}" for i in range(len(line_series))]
            line_values = line_series.tolist()
        else:
            line_labels = []
            line_values = []

        result = {
            "execution_time_ms": round((time.time() - start_time) * 1000, 2),
            "summary": {
                "rows": rows,
                "columns": columns
            },
            "charts": {
                "bar": {
                    "labels": bar_counts.index.tolist(),
                    "values": bar_counts.values.tolist()
                },
                "pie": {
                    "labels": pie_counts.index.tolist(),
                    "values": pie_counts.values.tolist()
                },
                "line": {
                    "labels": line_labels,
                    "values": line_values
                }
            }
        }

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.exception("Error")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )