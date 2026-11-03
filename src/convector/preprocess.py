from .gobbler import Preprocessor
from .config import logging, WIKIPATH, TOKENIZED_OUTPUT_DIR
from pathlib import Path
import re
import time
from multiprocessing import Pool, cpu_count

def preprocess(
    filepath: Path,
    destdir: Path = TOKENIZED_OUTPUT_DIR
):
    if not re.fullmatch(pattern = r'wiki_\d+', string = filepath.name):
        logging.info(f"Skipping {filepath}")
        return
    start = time.time()
    logging.info(f"Starting processing for {filepath.name}")

    destfile = destdir / filepath.relative_to(WIKIPATH)
    destfile.parent.mkdir(exist_ok = True, parents = True)
    preprocessor = Preprocessor(wikipath = filepath, outfile = destfile)
    # Run Preprocessor's SpaCy processing, outputting to file
    preprocessor.gobble()

    dur = time.time() - start
    logging.info(f"Processing of {filepath.name} complete | Time: {dur}")


if __name__ == "__main__":
    print("testing")

    rawfiles = [x for x in WIKIPATH.rglob('wiki_*') if x.is_file()]
    if not rawfiles:
        raise ValueError(f"No corpus files found in {WIKIPATH}")
    with Pool(
        max(1, min(len(rawfiles), cpu_count() - 1))
    ) as p:
        p.map(preprocess, rawfiles)
