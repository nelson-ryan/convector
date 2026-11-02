import spacy
import os
import re
from pathlib import Path
import time
from ..config import logging

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

