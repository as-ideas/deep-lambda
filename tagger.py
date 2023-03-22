import logging

from flair.data import Sentence
from flair.models import SequenceTagger

logger = logging.getLogger(__name__)


class Tagger:

    def __init__(self, model_path: str):
        logger.info(f'Initializing flair tagger from path: {model_path}')
        self._sequence_tagger = SequenceTagger.load(model_path)
        logger.info(f'Successfully initialized tagger from path: {model_path}')

    def __call__(self, text: str) -> str:
        sentence = Sentence(text)
        self._sequence_tagger.predict(sentence)
        result = '\n'.join([str(e) for e in sentence.get_spans('ner')])
        return result


if __name__ == '__main__':
    tagger = SequenceTagger.load('flair/ner-english')
    sentence = Sentence('George Washington went to Washington')
    tagger.predict(sentence)
    for entity in sentence.get_spans('ner'):
        print(entity)

    tagger.save('/tmp/my_ner_tagger.pt')