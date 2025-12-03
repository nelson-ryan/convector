# convector
from config import wikipath, tokenized_output_dir, tokenized_output, modelpath

# py
import os
import re
from pathlib import Path
import time
import logging

logging.basicConfig(
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filename = "log.log",
    level = logging.DEBUG
)

# nlp
import spacy
from gensim.models import Word2Vec
import multiprocessing


# gobble wikipedia files (omit <doc... and </doc> lines: skip title line that
# immediately follows <doc opening,

#TODO make a parent class for these two classes; there's just too much overlap
class Gobbler:
    """ Preprocessor to tokenize and lemmatize Wikipedia dump files
    """
    NLP = None # lazy loading
    def __init__(self, wikipath: Path, outfile: Path):
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
        start = time.time()
        logging.info(f"Gobbler Reading {path}")
        with open(path, mode = "r", encoding = "utf-8") as file:
            for doc in Gobbler.NLP.pipe(file, batch_size = 100):
                if re.match(pattern = r'^\w*$', string = doc.text):
                    # should exclude titles alone on a line, and empty lines
                    # doesn't *quite* work; titles ending in periods are kept
                    # and some empty lines still appear in output
                    continue
                if re.match(pattern = r'^<\\?.*>$', string = doc.text):
                    # exclude doc tags
                    continue
                for sentence in doc.sents:
                    yield [
                        token.lemma_.lower() for token in sentence
                        if not token.is_space
                        and not token.is_punct
                        and not token.is_stop
                    ]
        logging.info(f"Gobbler completed {path}")

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
        if not isinstance(self.path, Path):
            raise TypeError
        elif self.path.is_file():
            yield from self._yield_file(self.path)
        elif self.path.is_dir():
            yield from self._yield_dir(self.path)
        else:
            raise TypeError

    def _yield_file(self, path: Path):
        with open(path) as file:
            while line := file.readline():
                yield line.strip().split(" ")

    def _yield_dir(self, path: Path):
        for root, _, files in os.walk(path):
            for file in files:
                if file not in ["wiki_00", "wiki_01", "wiki_02", "wiki_03"]:
                # if not re.match(pattern = r'^wiki_\d\d$', string = file):
                    continue
                filepath = Path(root) / file
                yield from self._yield_file(filepath)

if __name__ == '__main__':

    # Preprocessing (tokenization/lemmatization) of Wikipedia extracted files
    if False:
    # TODO separate this altogether; it just takes too long on its own
    # if not tokenized_output.exists():
        logging.info("Postprocessing file not found. Starting preprocessing.")
        start = time.time()
        wikidump = Gobbler(wikipath, tokenized_output)
        wikidump.gobble()
        logging.info(f"Preprocessing complete. Time {time.time() - start}")
    wiki_processed = tokenized_output_dir

    # Train Word2Vec model
    logging.info("Starting model training.")
    start = time.time()
    sentences = TrainingIterator(wiki_processed)
    model = Word2Vec(
        sentences = sentences,
        sg = 0, # CBOW
        window = 5, # following Thurnbauer et al
        epochs = 5, # following Thurnbauer et al
        min_count = 10, # following Thurnbauer et al
        workers = multiprocessing.cpu_count() - 1, # (nearly) all of dems!
    )
    model.save(str(modelpath))
    logging.info(f"Model training complete. Time {time.time() - start}")
