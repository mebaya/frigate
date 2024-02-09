import io
import os
from typing import Union, Optional


import urllib3
from minio import Minio
from minio.error import S3Error

from .settings import CloudStorageObject
from ..const import RECORD_DIR

class RemoteStorageError:
    pass

class RemoteRecordStore:
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    def __init__(self, cloutauth: CloudStorageObject):
        self.cloutauth = cloutauth
        self.client = Minio(
            endpoint=cloutauth.endpoint,
            access_key=cloutauth.access_key,
            secret_key=cloutauth.secret_key,
            secure=False,
            http_client=urllib3.ProxyManager(
                f"http://{cloutauth.endpoint}",
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                maxsize=2,
                block=True)
        )
        for bucket in cloutauth.bucket:
            found = self.client.bucket_exists(bucket)
            if not found:
                self.client.make_bucket(bucket)
                print(f"ceated bucket {bucket}")

    def upload(self, recordfile: Union[str, io.BytesIO],  bucket: str, preffix: Optional[str] = RECORD_DIR):
        
        if bucket not in self.cloutauth.bucket:
            raise RemoteStorageError(f"invalid bucket name given: {bucket} expected one of: {self.cloutauth.bucket}")
        # plik
        if isinstance(recordfile, str):
            assert os.path.isfile(recordfile)
            if preffix is not None:
                filename = recordfile.replace(preffix, "")
                self.client.fput_object(bucket, filename, recordfile)
            else:
                filename = recordfile
            print(f"{recordfile} uploaded as object {filename} to bucket {bucket}.")
        # buffer
        else:
            self.client.put_object(bucket_name=bucket, object_name=filename, data=recordfile, length=-1)
            print(f"{filename} uploaded to bucket {bucket}")

if __name__ == "__main__":
    rrs = RemoteRecordStore(CloudStorageObject)
    rrs.upload("test.txt")

