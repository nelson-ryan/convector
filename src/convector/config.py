import logging

logging.basicConfig(
    format = "%(asctime)s | %(levelname)s | %(message)s",
    filename = "log.log",
    level = logging.INFO
)
logging.getLogger().addHandler(logging.StreamHandler())
logging = logging.getLogger()

from pathlib import Path

K = 5

ROOT = Path(__file__).parents[2]

WIKIPATH = ROOT / "wikidump" / "text_notemplate"

TOKENIZED_OUTPUT_DIR = ROOT / "wikidump" / "processed"

MODELROOT = ROOT / "model"
MODELPATH = MODELROOT / "convector.model"
