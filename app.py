import logging
from logging import INFO

import boto3
from typing import Dict, Any

from tagger import Tagger

logger = logging.getLogger(__name__)
logger.setLevel(level=INFO)


logger.info('Downloading model from bucket')
s3 = boto3.resource('s3')
bucket_name = 'deep-lambda'
bucket = s3.Bucket('deep-lambda')
bucket.download_file('my_ner_tagger.pt', '/tmp/my_ner_tagger.pt')
logger.info('Successfully downloaded model from bucket')
tagger = Tagger('/tmp/my_ner_tagger.pt')


def lambda_handler(event: Dict[str, Any], _: Dict[str, str]) -> Dict[str, str]:
    logger.info(f'Processing event: {event}')
    text = event['body']
    tag_result = tagger(text)
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {
            'content-type': 'application/json'
        },
        'body': tag_result
    }