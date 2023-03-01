import boto3
from typing import Dict, Any

from ner.tagger import Tagger

s3 = boto3.resource('s3')
bucket_name = 'deep-lambda'
bucket = s3.Bucket('deep-lambda')
bucket.download_file('my_ner_tagger.pt', '/tmp/my_ner_tagger.pt')
tagger = Tagger('/tmp/my_ner_tagger.pt')


def lambda_handler(event: Dict[str, Any], _: Dict[str, str]) -> str:
    text = event['text']
    return tagger(text)
