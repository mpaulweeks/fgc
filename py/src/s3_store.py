
import json
import boto3
from py.src.logger import log
from py.src.settings import (
    ENVARS,
    ensure_not_testing,
)

_GLOBAL_CACHE_NAME = "global_cache.json"
_GLOBAL_CACHE_PATH = "local/%s" % _GLOBAL_CACHE_NAME


def _connect_to_bucket():
    ensure_not_testing()
    session = boto3.Session(
        aws_access_key_id=ENVARS.aws_access_key_id,
        aws_secret_access_key=ENVARS.aws_secret_access_key,
        region_name=ENVARS.s3_region_name,
    )
    s3 = session.resource('s3')
    return s3.Bucket(ENVARS.s3_bucket_name)


def _upload_file(file_name, file_path):
    log("uploading %s to %s" % (file_path, file_name))
    with open(file_path, 'rb') as data:
        _connect_to_bucket().put_object(Key=file_name, Body=data)


def _download_file(file_name, file_path):
    log("downloading %s to %s" % (file_name, file_path))
    _connect_to_bucket().download_file(Key=file_name, Filename=file_path)


def upload_global_cache():
    _upload_file(_GLOBAL_CACHE_NAME, _GLOBAL_CACHE_PATH)


def download_global_cache():
    _download_file(_GLOBAL_CACHE_NAME, _GLOBAL_CACHE_PATH)


def load_global_cache_from_file():
    with open(_GLOBAL_CACHE_PATH) as file:
        return json.load(file)


def save_global_cache_dict_to_file(global_cache_dict):
    with open(_GLOBAL_CACHE_PATH, 'w') as file:
        json.dump(global_cache_dict, file)
    upload_global_cache()
