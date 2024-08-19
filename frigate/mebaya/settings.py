import os
from typing import List

class CloudStorageObject:
    bucket: List[str] = ["frigate-recordings", "frigate-snapshots"]
    access_key: str = os.environ.get("REMOTE_STORAGE_ACCESS_KEY", "jtSzTFTy2TH8WKSG2EWf")#"frigate-user"
    secret_key: str = os.environ.get("REMOTE_STORAGE_SECRET_KEY", "x8L81TtFn8OjsnhrbiyNhQ7dydE6TaYJxrgCVvNN") #"frigate-password"
    host: str = os.environ.get("REMOTE_STORAGE_ADDRESS", "192.168.8.124")
    port: int = int(os.environ.get("REMOTE_STORAGE_HOST", 9001))
    endpoint: str = f"{host}:{port}"

class PGSettings:
    POSTGRES_ADDRESS: str = os.environ.get("POSTGES_ADDRESS", "192.168.8.124")
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT", 5434))
    POSTGRES_DB: str = "camera_records"
    POSTGRES_USER: str = "mvision"
    POSTGRES_PASSWD: str = "mvisionqwerty1"

class FaceID:
    url: str = "http://192.168.8.124:8000/recognize"

