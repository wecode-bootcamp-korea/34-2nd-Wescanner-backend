import uuid
import boto3

class AWSFileUploader:
    def __init__(self, client, config):
        self.client = client
        self.config = config

    def upload(self, directory, file):
        file_id    = str(uuid.uuid4())
        extra_args = {'ContentType': file.content_type}
        key        = f"{directory}/{file_id}"

        self.client.upload_fileobj(file, self.config["bucket_name"], key, ExtraArgs = extra_args)
        
        return f'https://{self.config["bucket_name"]}.s3.{self.region}.amazonaws.com/{image_url}'

    def delete(self, bucket_name, key):
        self.client.delete_object(Bucket=self.config["bucket_name"], Key=key)


class FileHandler:
    def __init__(self, client):
        self.client = client

    def upload(self, directory, file):
        return self.client.upload(directory, file)

    def delete(self, bucket_name, file_name):
        return self.client.delete(bucket_name, file_name)