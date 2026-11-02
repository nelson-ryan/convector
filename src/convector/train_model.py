from .gobbler import ReaderIterator
from .config import (
    logging,
    TOKENIZED_OUTPUT_DIR,
    MODELPATH,
    K
)
import time

from gensim.models import Word2Vec
import multiprocessing


# Train Word2Vec model
logging.info("Starting model training.")
start = time.time()
sentences = ReaderIterator(TOKENIZED_OUTPUT_DIR)
model = Word2Vec(
    sentences = sentences,
    sg = 0,         # CBOW
    window = K,     # 5, following Thurnbauer et al
    epochs = 5,     # following Thurnbauer et al
    min_count = 10, # following Thurnbauer et al
    workers = multiprocessing.cpu_count() - 1,
)
model.save(str(MODELPATH))
logging.info(f"Model training complete. Time {time.time() - start}")

