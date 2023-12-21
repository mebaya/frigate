import os

import urllib3
from minio import Minio
from minio.error import S3Error

from .settings import CloudStorageObject
from ..const import RECORD_DIR

class RemoteRecordStore:
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    def __init__(self, cloutauth: CloudStorageObject):
        self.client = Minio(
            endpoint=cloutauth.endpoint,
            access_key=cloutauth.access_key,
            secret_key=cloutauth.secret_key,
            secure=False,
            http_client=urllib3.ProxyManager(
                f"http://{cloutauth.endpoint}",
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT)
        )
        self.bucket = cloutauth.bucket
        found = self.client.bucket_exists(self.bucket)
        if not found:
            self.client.make_bucket(self.bucket)
        else:
            print(f"Bucket '{self.bucket}' already exists")

    def upload(self, recordfile: str):
        assert os.path.isfile(recordfile)
        filename = recordfile.replace(RECORD_DIR, "")
        self.client.fput_object(
            self.bucket, filename, recordfile,
        )
        print(
            f"{recordfile} is successfully uploaded as object {filename} to bucket {self.bucket}."
        )

if __name__ == "__main__":
    rrs = RemoteRecordStore(CloudStorageObject)
    rrs.upload("test.txt")

