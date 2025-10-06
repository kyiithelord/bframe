from minio import Minio
from .config import settings

_client = None

def get_client() -> Minio:
    global _client
    if _client is None:
        endpoint = settings.MINIO_ENDPOINT
        access_key = settings.MINIO_ACCESS_KEY
        secret_key = settings.MINIO_SECRET_KEY
        secure = False if endpoint.startswith("minio:") or ":9000" in endpoint else True
        _client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        # ensure bucket
        if not _client.bucket_exists(settings.MINIO_BUCKET):
            _client.make_bucket(settings.MINIO_BUCKET)
    return _client


def put_object(name: str, data, length: int, content_type: str | None = None) -> str:
    client = get_client()
    client.put_object(settings.MINIO_BUCKET, name, data, length, content_type=content_type)
    # Return a URL (assuming console is not public; presign GET for simplicity)
    url = client.presigned_get_object(settings.MINIO_BUCKET, name)
    return url
