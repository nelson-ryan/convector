import spacy
import os
import re
from pathlib import Path
import time
from convector.config import logging

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
                if not re.match(pattern = r'^wiki_\d\d$', string = file):
                    continue
                filepath = Path(root) / file
                yield from self._gobble_file(filepath)


