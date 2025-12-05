# convector
from config import (
    wikipath, tokenized_output_dir, tokenized_output, modelpath, K
)
from gobbler import Gobbler, TrainingIterator

# py
from pathlib import Path
import time
import logging

logging.basicConfig(
    format = "%(asctime)s | %(levelname)s | %(message)s",
    filename = "log.log",
    level = logging.INFO
)
logging.getLogger().addHandler(logging.StreamHandler())

# nlp
from gensim.models import Word2Vec
import multiprocessing

def context_vectors(words):
    reader = TrainingIterator(tokenized_output_dir)
    word = "bangle"
    outfile = Path(f"{word}.txt")
    with open(outfile, mode = "w", encoding = "utf-8") as file:
        for line in reader:
            try:
                i = line.index(word)
            except ValueError:
                continue
            s = max(0, i - K)
            e = min(len(line), i + K + 1)
            context = line[s:i] + line[i+1:e]
            file.write(" ".join(line) + "\n")
            print(context)

if __name__ == '__main__':

    # Preprocessing (tokenization/lemmatization) of Wikipedia extracted files
    if False:
    # TODO separate this altogether; it just takes too long on its own
    # if not tokenized_output.exists():
        logging.info("Postprocessing file not found. Starting preprocessing.")
        start = time.time()
        wikidump = Gobbler(wikipath, tokenized_output)
        wikidump.gobble()
        logging.info(f"Preprocessing complete. Time {time.time() - start}")
    wiki_processed = tokenized_output_dir

    # Train Word2Vec model
    logging.info("Starting model training.")
    start = time.time()
    sentences = TrainingIterator(wiki_processed)
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

    # TODO get from Connections
    words = ["bangle", "chain", "charm", "ring",
     #        "event", "function", "party", "reception",
     #        "appeal", "campaign", "lobby", "press",
     #        "iron", "macho", "piano", "rocket"
    ]
    #context_vectors(words)
