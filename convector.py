
import spacy
from gensim.models import Word2Vec

from config import wikipath

# gobble wikipedia files (omit <doc... and </doc> lines: skip title line that
# immediately follows <doc opening,

class WikiGobbler:
    NLP = None # lazy loading
    def __init__(self, path):
        self.wikipath = path
        if not WikiGobbler.NLP:
            WikiGobbler.NLP = spacy.load("en_core_web_md")

    def __iter__(self):
        if wikipath.is_file():
            self._gobble_file()
        pass

    def _gobble_file(self):
        raise NotImplementedError

    def _gobble_dir(self):
        raise NotImplementedError

