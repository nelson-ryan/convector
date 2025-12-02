# convector
from config import wikipath

# py
import os
import re
from pathlib import Path

# nlp
import spacy
from gensim.models import Word2Vec
import multiprocessing


# gobble wikipedia files (omit <doc... and </doc> lines: skip title line that
# immediately follows <doc opening,

class Gobbler:
    """ Wikipedia-dump-Gobbler
        Serves as a preprocessor and iterator to feed into Word2Vec training
    """
    NLP = None # lazy loading
    def __init__(self, path: Path):
        """ 
            path (Path): parent path to extracted wikipedia dump
            OR path to single wikipedia file
        """
        self.wikipath = path
        if not Gobbler.NLP: # lazy loading of spacy pipeline
            Gobbler.NLP = spacy.load("en_core_web_md")

    def __iter__(self):
        if self.wikipath.is_file():
            yield from self._gobble_file(self.wikipath)
        elif self.wikipath.is_dir():
            yield from self._gobble_dir(self.wikipath)
        else:
            raise TypeError

    def _gobble_file(self, path):
        """ Reads all Wikipedia lines and produces lemmatized tokens.
            path (Path): individual wikipedia dump file
        """
        with open(path, mode = "r", encoding = "utf-8") as file:
            for doc in Gobbler.NLP.pipe(file, batch_size = 50):
                if len(doc) < 2: # should exclude titles alone on a line
                    continue
                if re.match(pattern = r'^<\\?.*>$', string = doc.text):
                    # exlude doc tags
                    continue
                for sentence in doc.sents:
                    yield [
                        token.lemma_.lower() for token in sentence
                        if not token.is_space and not token.is_punct
                    ]

    def _gobble_dir(self, path):
        for root, _, files in os.walk(path):
            for file in files:
                if not re.match(pattern = r'^wiki_\d\d$', string = file):
                    # should never apply, but whatev
                    continue
                filepath = Path(root) / file
                yield from self._gobble_file(filepath)

if __name__ == '__main__':
    wikidump = Gobbler(wikipath)

    model = Word2Vec(
        sentences = wikidump,
        sg = 0, # CBOW
        window = 5, # following Thurnbauer et al
        epochs = 5, # following Thurnbauer et al
        min_count = 10, # following Thurnbauer et al
        workers = multiprocessing.cpu_count(), # all of dems!
    )
    model.save("convector.model")
