from pathlib import Path

K = 5

try:
    base = Path(__file__).parent
except NameError:
    base = Path().home() / "hlt" / "convector"

# wikipath = base / "wikidump" / "text_notemplate" / "AA" / "wiki_00"
wikipath = base / "wikidump" / "text_notemplate"

tokenized_output_dir = base / "wikidump"
tokenized_output = tokenized_output_dir / "tokenized_wiki.txt"

modelpath = base / "model" / "convector.model"

