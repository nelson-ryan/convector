from functools import cached_property
from convector.gobbler import Preprocessor, ReaderIterator
from convector.config import modelpath, tokenized_output_dir, K
from gensim.models import Word2Vec
import numpy as np
from convector.config import logging


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
    def contextword_indices(self) -> dict[str, list[list]]:
        return self._get_contextword_indices()

    def _get_contextword_indices(self) -> dict[str, list[list]]:
        reader = ReaderIterator(tokenized_output_dir)
        result = {}
        for line in reader:
            for lemma in self.lemmas:
                if lemma in line:
                    i = line.index(lemma)
                else:
                    continue
                s = max(0, i - K)
                e = min(len(line), i + K + 1)
                context = line[s:i] + line[i+1:e]
                context = [
                    self._model.wv.get_index(word) for word in context
                    if word in self._model.wv
                ]
                if len(context) > 0:
                    result.setdefault(lemma, []).append(context)
        return result

    def _calculate_contextvectors(self):
        contextvectors = {}
        for cardword, contexts in self.contextword_indices.items():
            for context in contexts:
                contextvector = np.mean(
                    self._model.wv.vectors[context],
                    axis = 0
                )
                contextvectors.setdefault(cardword, []).append(contextvector)
        return contextvectors

