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
LOCAL_PATH = "data/All_Diets.csv"

def main():
    bsc = BlobServiceClient.from_connection_string(CONNECT_STR)

    # Create container if not exists
    container_client = bsc.get_container_client(CONTAINER)
    try:
        container_client.create_container()
        print(f"Created container: {CONTAINER}")
    except Exception:
        print(f"Container already exists: {CONTAINER}")

    blob_client = container_client.get_blob_client(BLOB_NAME)
    with open(LOCAL_PATH, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)

    print(f"Uploaded {LOCAL_PATH} -> {CONTAINER}/{BLOB_NAME}")

if __name__ == "__main__":
    main()
