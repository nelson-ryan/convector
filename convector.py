# convector
from config import tokenized_output_dir, K
from gobbler import TrainingIterator

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

if __name__ == '__main__':

    # TODO get from Connections
    words = ["bangle", "chain", "charm", "ring",
     #        "event", "function", "party", "reception",
     #        "appeal", "campaign", "lobby", "press",
     #        "iron", "macho", "piano", "rocket"
    ]
    # wl = WordList(words)
