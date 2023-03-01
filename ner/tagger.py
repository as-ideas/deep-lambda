from flair.data import Sentence
from flair.models import SequenceTagger


class Tagger:

    def __init__(self, model_path: str):
        self.flair_tagger = SequenceTagger.load(model_path)

    def __call__(self, text: str) -> str:
        sentence = Sentence(text)
        self.flair_tagger.predict(sentence)
        result = '\n'.join([str(e) for e in sentence.get_spans('ner')])
        return result


if __name__ == '__main__':
    tagger = SequenceTagger.load('flair/ner-english')
    sentence = Sentence('George Washington went to Washington')
    tagger.predict(sentence)
    for entity in sentence.get_spans('ner'):
        print(entity)

    tagger.save('/tmp/my_ner_tagger.pt')