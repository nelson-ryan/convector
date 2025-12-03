import sys
from pathlib import Path
import re

name =  f"wiki_{int(sys.argv[1]):02d}"
if not re.match(pattern = r'wiki_\d\d', string = name):
    raise TypeError
source = Path(__file__).parent / "wikidump" / "text_notemplate" / "AA" / name
if not source.exists():
    raise FileNotFoundError("sourcefile")
dest = Path(__file__).parent / "wikidump" / "processed" / name
if not dest.parent.exists():
    raise FileNotFoundError("destdir")


from convector import Gobbler

gobbler = Gobbler(wikipath = source, outfile = dest)
gobbler.gobble()
