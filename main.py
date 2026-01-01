# convector
from convector.config import logging
from convector.config import modelpath
from convector.wordlist import WordList
from gensim.models import Word2Vec
import numpy as np
import multiprocessing

# py
import time

from sklearn.cluster import DBSCAN


if __name__ == '__main__':

    # TODO get from Connections
    # 2025-10-15
    words = ["infinity", "kiddie", "kidney", # "olympic", # types of pools
            "bravo", "delta", "golf", "lima", # NATO alphabet
            "bronco", "fiesta", "mustang", "pinto", # Ford models
            "elephant", # "great",
             "navy", "vacuum" # __SEAL
    ]
    model = Word2Vec.load(str(modelpath))
    wl = WordList(words, model)
    _ = wl.contextvectors # Not pretty, but this caches them before use below

    logging.info("Starting DBSCAN fitting")
    start = time.time()
    clustered_centroids = []
    for word in words:
        dbscan = DBSCAN(
            eps = .20, min_samples = 10, metric = "cosine",
            n_jobs = multiprocessing.cpu_count() - 1
        )
        contextvectors = np.array(wl.contextvectors[word])
        fitstart = time.time()
        logging.info(f"Fitting '{word}' to new DBSCAN model, with {len(wl.contextvectors[word])} instances")
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
    for word in words:
        print(word, len([x for x in clustered_centroids if x[0] == word]))

    import pickle
    # with open("clustered_centroids.pickle", "wb") as pfile:
     #    pickle.dump(clustered_centroids, pfile)
    with open("clustered_centroids.pickle", "rb") as pfile:
        clustered_centroids = pickle.load(pfile)


    def pnorm(v, p = 2):
        v = np.array(v)
        return np.power(np.power(v + 1e-8, p).sum(), 1/p)
    def cosim(a, b):
        return np.dot(a, b) / (pnorm(a) * pnorm(b))

    res = []
    for word in words:
        alltarget = [x for x in clustered_centroids if x[0] == word]
        compwords = [x for x in clustered_centroids if x[0] != word]
        for target in alltarget:
            for compword in compwords:
                sim = cosim(target[2], compword[2])
                res.append((word, compword[0], sim))
    res.sort(key = lambda x: x[2], reverse = True)
    for word in words:
        print("\n" + word)
        print(
            *[(comp, sim) for wd, comp, sim in res if wd == word][:3],
            sep = "\n"
        )
