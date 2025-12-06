# convector
from convector.config import logging
from convector.config import tokenized_output_dir, K, modelpath
from convector.gobbler import ReaderIterator
from convector.wordlist import WordList
from gensim.models import Word2Vec
import numpy as np
import multiprocessing

# py
from pathlib import Path
import time

from sklearn.cluster import DBSCAN


if __name__ == '__main__':

    # TODO get from Connections
    words = ["bangle", "chain", "charm", "ring",
     #        "event", "function", "party", "reception",
     #        "appeal", "campaign", "lobby", "press",
     #        "iron", "macho", "piano", "rocket"
    ]
    model = Word2Vec.load(str(modelpath))
    wl = WordList(words, model)

    logging.info("Starting DBSCAN fitting")
    start = time.time()
    clustered_centroids = []
    for word in words:
        dbscan = DBSCAN(
            eps = .21, min_samples = 15, metric = "cosine",
            n_jobs = multiprocessing.cpu_count() - 1
        )
        contextvectors = np.array(wl.contextvectors[word])
        fitstart = time.time()
        logging.info(f"Fitting {word} to new DBSCAN model")
        dbscan.fit(wl.contextvectors[word])
        logging.info(f"Duration for {word}: {time.time() - fitstart}")

        for label in set(dbscan.labels_):
            if label == -1: # skip the noise label
                continue
            # A little cryptic, this conditional indexes/slices `contextvectors`
            # where the DBSCAN assigned label matches the loop's `label`
            clustervectors = contextvectors[dbscan.labels_ == label]
            centroid = np.mean(clustervectors, axis = 0)
            clustered_centroids.append(
                (word, label, centroid)
            )
    logging.info(f"DBSCAN total duration: {time.time() - start}")
