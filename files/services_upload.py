import boto3

from django.core import settings

# analizar is esto expone vulnerabilidad
def generate_url_uploadfiles(file_name, file_type, expliration=3600):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    presigned_post = s3_client.generate_presigned_post(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=file_name,
        Fields={"Content-Type": file_type},
        Conditions=[
            {"Content-Type": file_type}
        ],
        ExpiresIn=expiration
    )
    return presigned_post
