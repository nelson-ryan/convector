from functools import cached_property
from gobbler import Preprocessor, TrainingIterator
from config import modelpath, tokenized_output_dir, K
from gensim.models import Word2Vec
import numpy as np
import logging

logging.basicConfig(
    format = "%(asctime)s | %(levelname)s | %(message)s",
    filename = "log.log",
    level = logging.INFO
)
logging.getLogger().addHandler(logging.StreamHandler())


class WordList:
    def __init__(self, wordlist: list, model: Word2Vec):
        self.wordlist = wordlist
        self._model = model

    @cached_property
    def lemmas(self):
        lemmas = []
        docs = Preprocessor.NLP.pipe(self.wordlist)
        for doc in docs:
            for word in doc:
                lemmas.append(word.lemma_.lower())
        return lemmas

    @cached_property
    def contextvectors(self):
        return self._calculate_contextvectors()

    @cached_property
    def contextwords(self) -> dict[str, list[list]]:
        return self._get_contextwords()

    def _get_contextwords(self) -> dict[str, list[list]]:
        reader = TrainingIterator(tokenized_output_dir)
        result = {}
        for line in reader:
            for lemma in self.lemmas:
                try:
                    i = line.index(lemma)
                except ValueError:
                    continue
                s = max(0, i - K)
                e = min(len(line), i + K + 1)
                context = line[s:i] + line[i+1:e]
                result.setdefault(lemma, []).append(context)
        return result

    def _calculate_contextvectors(self):
        contextvectors = {}
        for cardword, contexts in self.contextwords.items():
            for context in contexts:
                wordindices = [
                    self._model.wv.get_index(word) for word in context
                    if word in self._model.wv
                ]
                contextvector = np.mean(
                    self._model.wv.vectors[wordindices],
                    axis = 0
                )
                if len(wordindices) < 1:
                    continue
                contextvectors.setdefault(cardword, []).append(contextvector)
        return contextvectors

if __name__ == "__main__":
    model = Word2Vec.load(str(modelpath))
    word = "bangle"
    wl = WordList([word], model)
    len(wl.contextwords[word])
    len(wl.contextvectors[word])


