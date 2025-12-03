# convector
from config import wikipath, tokenized_output

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
    """ Preprocessor to tokenize and lemmatize Wikipedia dump files
    """
    NLP = None # lazy loading
    def __init__(self, wikipath: Path, outfile: Path = tokenized_output):
        """ wikipath (Path): parent path to extracted wikipedia dump
            OR path to single extracted wikipedia file (for testing)

            out_file (Path): path for singular output, lemmatized text file
        """
        self.wikipath = wikipath
        self.outfile = outfile
        if not Gobbler.NLP: # lazy loading of spacy pipeline
            print("Loading SpaCy")
            Gobbler.NLP = spacy.load("en_core_web_md")

    def gobble(self):
        with open(self.outfile, mode = "w", encoding = "utf-8") as file:
            for line in self:
                file.write(" ".join(line) + "\n")

    def __iter__(self):
        if not isinstance(self.wikipath, Path):
            raise TypeError
        elif self.wikipath.is_file():
            yield from self._gobble_file(self.wikipath)
        elif self.wikipath.is_dir():
            yield from self._gobble_dir(self.wikipath)
        else:
            raise TypeError

    def _gobble_file(self, path):
        """ Reads all Wikipedia lines and produces lemmatized tokens.
            path (Path): individual wikipedia dump file
        """
        print(f"Reading {path}")
        with open(path, mode = "r", encoding = "utf-8") as file:
            for doc in Gobbler.NLP.pipe(file, batch_size = 100):
                if re.match(pattern = r'^\w*$', string = doc.text):
                    # should exclude titles alone on a line, and empty lines
                    continue
                if re.match(pattern = r'^<\\?.*>$', string = doc.text):
                    # exclude doc tags
                    continue
                for sentence in doc.sents:
                    yield [
                        token.lemma_.lower() for token in sentence
                        if not token.is_space
                        and not token.is_punct
                        and not  token.is_stop
                    ]

    def _gobble_dir(self, path):
        for root, _, files in os.walk(path):
            for file in files:
                if not re.match(pattern = r'^wiki_\d\d$', string = file):
                    # should never apply, but whatev
                    continue
                filepath = Path(root) / file
                yield from self._gobble_file(filepath)

class TrainingIterator:
    def __init__(self, path: Path):
        self.path = path
    def __iter__(self):
        with open(self.path) as file:
            while line := file.readline():
                yield line.strip().split(" ")

if __name__ == '__main__':

    print(wikipath)

    # Preprocessing (tokenization/lemmatization) of Wikipedia extracted files
    wikidump = Gobbler(wikipath)
    wikidump.gobble()
    wiki_processed = wikidump.outfile

    # Train Word2Vec model
    sentences = TrainingIterator(wiki_processed)
    model = Word2Vec(
        sentences = sentences,
        sg = 0, # CBOW
        window = 5, # following Thurnbauer et al
        epochs = 5, # following Thurnbauer et al
        min_count = 10, # following Thurnbauer et al
        workers = multiprocessing.cpu_count() - 1, # (nearly) all of dems!
    )
    model.save("convector.model")
