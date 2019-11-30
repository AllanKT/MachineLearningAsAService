
# -*- coding: utf-8 -*-

"""Script to storage files in S3."""

import boto3
from botocore.exceptions import ClientError
# from settings.log import logger
from pprint import pprint
import os


class S3():
    """Storage files in S3."""
    def __init__(self, bucket, key, secret):
        """Instance class."""
        self.bucket = bucket
        self.client = boto3.client('s3',
                    aws_access_key_id=key,
                    aws_secret_access_key=secret)
        self.resource = boto3.resource('s3',
                                        aws_access_key_id=key,
                                        aws_secret_access_key=secret)
        self.__create_bucket()

    def __create_bucket(self):
        """Function for create a bucket by name from AmazonS3."""
        try:
            # if not exists, create it, else, clean it
            if not self.__validate_bucket():
                # logger.warning(f"Bucket {self.bucket} não encontrado")
                self.client.create_bucket(Bucket=self.bucket)
            # logger.debug(f"Bucket {self.bucket} criado com sucesso")
            return True
        except Exception as e:
            # logger.exception(e)
            return False

    def __validate_bucket(self):
        """Function for validate if the enviroment variable bucket exist in client."""
        try:
            # logger.debug("Takes all buckets that exist on the client")
            response = self.client.list_buckets()
            # logger.debug("Validates the existence of the bucket of the environment variable bucket")
            for bucket in response['Buckets']:
                if bucket['Name'] == self.bucket:
                    return True
            return False
        except Exception as e:
            # logger.exception(e)
            return False

    def upload_s3(self, filename, key):
        """Upload file to storage."""
        try:
            if self.__validate_bucket():
                self.client.upload_file(filename,
                                        self.bucket,
                                        key,
                                        ExtraArgs={
                                            'ACL':'public-read'
                                        }) 
                # logger.debug(f"upload file {filename} successfully from bucket {self.bucket} in AmazonS3 with the key {key}")
                return True, f"upload file {filename} successfully from bucket {self.bucket} in AmazonS3 with the key {key}"
            # logger.warning(f"upload file {filename} failed from bucket {self.bucket} in AmazonS3 with the key {key}")
            return False, f"upload file {filename} failed from bucket {self.bucket} in AmazonS3 with the key {key}"
        except Exception as e:
            # logger.exception(e)
            return False, str(e)
