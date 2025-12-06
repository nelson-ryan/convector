from convector.gobbler import Preprocessor
from convector.config import logging
import sys
from pathlib import Path
import re
import time

start = time.time()
# using command line argument, pattern of extracted Wikipedia files
name =  f"wiki_{int(sys.argv[1]):02d}"
# this is silly because I just defined `name` to match the pattern
if not re.match(pattern = r'wiki_\d\d', string = name):
    raise TypeError
logging.info(f"Starting processing for {name}")

# get full path to file
source = Path(__file__).parent / "wikidump" / "text_notemplate" / "AA" / name
if not source.exists():
    raise FileNotFoundError("sourcefile")

# define output file
dest = Path(__file__).parent / "wikidump" / "processed" / name
if not dest.parent.exists():
    raise FileNotFoundError("destdir")

# Run Preprocessor's SpaCy processing, outputting to file
preprocessor = Preprocessor(wikipath = source, outfile = dest)
preprocessor.gobble()
logging.info(f"Processing of {name} complete | Time: {time.time() - start}")
