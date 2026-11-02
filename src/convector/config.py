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

# wikipath = ROOT / "wikidump" / "text_notemplate" / "AA" / "wiki_00"
wikipath = ROOT / "wikidump" / "text_notemplate"

tokenized_output_dir = ROOT / "wikidump" / "processed"

modelpath = ROOT / "model" / "convector.model"

