# convector
from config import logging
from config import tokenized_output_dir, K
from gobbler import TrainingIterator

# py
from pathlib import Path
import time


if __name__ == '__main__':

    # TODO get from Connections
    words = ["bangle", "chain", "charm", "ring",
     #        "event", "function", "party", "reception",
     #        "appeal", "campaign", "lobby", "press",
     #        "iron", "macho", "piano", "rocket"
    ]
    # wl = WordList(words)
