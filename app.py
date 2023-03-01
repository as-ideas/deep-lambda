from typing import Dict, Any

from ner.tagger import Tagger


tagger = Tagger('flair/ner-english"')


def lambda_handler(event: Dict[str, Any], _: Dict[str, str]) -> str:
    text = event['text']
    return tagger(text)
