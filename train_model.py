from convector.gobbler import ReaderIterator
from convector.config import tokenized_output_dir, modelpath, K
from convector.config import logging
import time

from gensim.models import Word2Vec
import multiprocessing


# Train Word2Vec model
logging.info("Starting model training.")
start = time.time()
sentences = ReaderIterator(tokenized_output_dir)
model = Word2Vec(
    sentences = sentences,
    sg = 0, # CBOW
    window = K, # 5, following Thurnbauer et al
    epochs = 5, # following Thurnbauer et al
    min_count = 10, # following Thurnbauer et al
    workers = multiprocessing.cpu_count() - 1, # (nearly) all of dems!
)
model.save(str(modelpath))
logging.info(f"Model training complete. Time {time.time() - start}")

