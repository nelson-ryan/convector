from pathlib import Path

try:
    base = Path(__file__).parent
except NameError:
    base = Path().home() / "hlt" / "convector"
wikipath = base / "wikidump" / "text_notemplate" / "AA" / "wiki_00"
# wikipath = base / "wikidump" / "text_notemplate"
tokenized_output = base / "wikidump" / "tokenized_wiki.txt"


