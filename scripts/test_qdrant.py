from dotenv import load_dotenv
import os
import sys

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL:
    print("QDRANT_URL not set")
    sys.exit(2)

print("Qdrant URL:", QDRANT_URL)

try:
    from qdrant_client import QdrantClient
except Exception as e:
    print("qdrant_client import failed:", e)
    raise

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

print("Connected, attempting to list collections...")
try:
    # Try the common client method
    collections = None
    if hasattr(client, 'get_collections'):
        collections = client.get_collections()
    elif hasattr(client, 'collections_api') and hasattr(client.collections_api, 'list_collections'):
        collections = client.collections_api.list_collections()
    else:
        print("No known method to list collections on this client object")

    print("Collections:", collections)
except Exception as e:
    print("Failed to list collections:", e)
    raise
