import uuid
import boto3

class S3_Client:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, region):
        s3 = boto3.client('s3',
                          aws_access_key_id     = aws_access_key_id,
                          aws_secret_access_key = aws_secret_access_key)

        self.s3client    = s3
        self.bucket_name = bucket_name
        self.region      = region

    def upload(self, directory, file):
        file_id    = str(uuid.uuid4())
        extra_args = {'ContentType': file.content_type}
        image_url  = f"{directory}/{file_id}"

        self.s3client.upload_fileobj(file, self.bucket_name, image_url, ExtraArgs = extra_args)
        
        return f'https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{image_url}'

    def delete(self, bucket_name, image_name):
        self.s3client.delete_object(Bucket=bucket_name, Key=image_name)


class FileHandler:
    def __init__(self, client):
        self.client = client

    def upload(self, directory, file):
        return self.client.upload(directory, file)

    def delete(self, bucket_name, file_name):
        return self.client.delete(bucket_name, file_name)