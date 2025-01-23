from io import BytesIO
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from logger.logger import CustomLogger


class S3Client:
    """
    A client to handle AWS S3 operations.

    Attributes:
        bucket_name (str): The name of the S3 bucket.
        logger: Logger instance for logging operations.
    """

    def __init__(self, aws_access_key_id, aws_secret_access_key, region: str, logger: CustomLogger):
        self.logger = logger
        session = boto3.Session()
        self.s3 = session.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

    def upload_file(self, image: str, object_name: str = None, bucket_name: str = None):
        """
        Uploads a file to the S3 bucket.

        Args:
            file_path (str): The path of the file to upload.
            object_name (str): The S3 object name. If None, uses the file name.

        Returns:
            str: The URL of the uploaded file.

        Raises:
            ValueError: If the file does not exist or upload fails.
        """
        try:
            # Upload the file to the S3 bucket
            image_file = BytesIO(image)
            self.s3.Bucket(bucket_name).put_object(Key=object_name, Body=image_file)
            self.logger.info(f"Image uploaded successfully as '{object_name}'.")

            # Construct the file URL
            file_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
            self.logger.info(f"File URL: {file_url}")

            return file_url

        except (BotoCoreError, ClientError) as e:
            self.logger.error(f"Error uploading file to S3: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            raise

    def get_signed_url(self, bucket_name: str, key: str, expiration: int):
        """
        Generates a pre-signed URL for the given S3 object.

        Args:
            bucket (str): The name of the S3 bucket.
            key (str): The key of the S3 object.
            expiration (int): The expiration time of the URL in seconds.

        Returns:
            str: The pre-signed URL.

        Raises:
            ValueError: If the URL generation fails.
        """
        try:
            # Generate the pre-signed URL
            url = self.s3.meta.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            self.logger.info(f"Pre-signed URL generated successfully for '{key}'.")
            return url
        except ClientError as e:
            self.logger.error(f"Error generating pre-signed URL: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Validation error: {e}")
            raise
