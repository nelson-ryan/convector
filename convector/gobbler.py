import spacy
import os
import re
from pathlib import Path
import time
from convector.config import logging


class Gobbler:
    """ Parent class for iterators
        path (Path): path to source, file or dir
    """
    def __init__(self, source):
        self.source = source

    def __iter__(self):
        if isinstance(self.source, Path):
            if self.source.is_file():
                yield from self._gobble_file(self.source)
            if self.source.is_dir():
                yield from self._gobble_dir(self.source)
        elif isinstance(self.source, list):
            yield from self._process(self.source)

    def _gobble_file(self, source):
        raise NotImplementedError

    def _gobble_dir(self, source):
        raise NotImplementedError

    def _process(self, source):
        raise NotImplementedError


#TODO make a parent class for these two classes; there's just too much overlap
class Preprocessor:
    """ Preprocessor to tokenize and lemmatize Wikipedia dump files
    """
    NLP = spacy.load("en_core_web_md")
    def __init__(self, wikipath: Path, outfile: Path):
        """ wikipath (Path): parent path to extracted wikipedia dump
            OR path to single extracted wikipedia file (for testing)

            out_file (Path): path for singular output, lemmatized text file
        """
        self.wikipath = wikipath
        self.outfile = outfile

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
        logging.info(f"Preprocessor reading {path}")
        with open(path, mode = "r", encoding = "utf-8") as file:
            for doc in Preprocessor.NLP.pipe(file, batch_size = 100):
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
        logging.info(
            f"Preprocessor completed {path} | Time: {time.time() - start}"
        )

    def _gobble_dir(self, path):
        for root, _, files in os.walk(path):
            for file in files:
                if not re.match(pattern = r'^wiki_\d\d$', string = file):
                    # should never apply, but whatev
                    continue
                filepath = Path(root) / file
                yield from self._gobble_file(filepath)

class ReaderIterator:
    def __init__(self, path: Path):
        self.path = path

    def __iter__(self):
        if not isinstance(self.path, Path):
            raise TypeError
        elif self.path.is_file():
            yield from self._gobble_file(self.path)
        elif self.path.is_dir():
            yield from self._gobble_dir(self.path)
        else:
            raise TypeError

    def _gobble_file(self, path: Path):
        logging.info(f"Reading {path}")
        with open(path) as file:
            while line := file.readline():
                yield line.strip().split(" ")

    def _gobble_dir(self, path: Path):
        for root, _, files in os.walk(path):
            for file in files:
                # if file not in ["wiki_18"]:
                if not re.match(pattern = r'^wiki_\d\d$', string = file):
                    continue
                filepath = Path(root) / file
                yield from self._gobble_file(filepath)


