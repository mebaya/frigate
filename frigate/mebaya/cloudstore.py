import os
from minio import Minio
from minio.error import S3Error


class CloudRecords:
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    def __init__(self, access_key: str, secret_key: str, bucket: str):
        self.client = Minio(
            "play.min.io",
            access_key=access_key,
            secret_key=secret_key,
        )
        self.bucket = bucket
        found = self.client.bucket_exists(self.bucket)
        if not found:
            self.client.make_bucket(self.bucket)
        else:
            print(f"Bucket '{self.bucket}' already exists")

    def upload(self, recordfile: str):
        assert os.path.isfile(recordfile)
        flatname = recordfile.replace(r"/", r"_")
        self.client.fput_object(
            self.bucket, flatname, recordfile,
        )
        print(
            f"{recordfile} is successfully uploaded as object {flatname} to bucket {self.bucket}."
        )

