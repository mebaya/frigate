import os

class CloudStorageObject:
    bucket: str = "frigate-recordings"
    access_key: str = "jtSzTFTy2TH8WKSG2EWf"#"frigate-user"
    secret_key: str = "x8L81TtFn8OjsnhrbiyNhQ7dydE6TaYJxrgCVvNN"#"frigate-password"
    host: str = "192.168.8.121"
    port: int = 9000
    endpoint: str = f"{host}:{port}"

class PGSettings:
    POSTGRES_ADDRESS: str = os.environ.get("POSTGES_ADDRESS", "192.168.8.121")
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = "camera_records"
    POSTGRES_USER: str = "mvision"
    POSTGRES_PASSWD: str = "mvisionqwerty1"

