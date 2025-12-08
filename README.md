
## Setup

The included Dockerfile includes Python dependencies, including wikiextractor.

``` bash
docker build -t convectorimage .
docker run -it --name convector convectorimage
```

## Wikipedia

This project used the 2025-11-01 Wikipedia dump; the file is directly available
[here (23GB).](https://dumps.wikimedia.org/enwiki/20251120/enwiki-20251120-pages-articles-multistream.xml.bz2)

Needless to say, its size precludes its inclusion here.

### Extraction (wikiextractor)

The Wikipedia dump must also be extracted; for this,
I used [wikipediaextractor](https://github.com/attardi/wikiextractor).

The Dockerfile includes a compatibility fix for Python 3.12 (necessary for
wikiextractor version v3.0.9).

This is resolved in [commit ab8988e](https://github.com/attardi/wikiextractor/commit/ab8988ebfa9e4557411f3d4c0f4ccda139e18875)'s `extract.py` file.  
This should be resolvable either by installing the commit directly
(as in the Dockerfile)  
```bash
pip install git+https://github.com/attardi/wikiextractor.git@ab8988ebfa9e4557411f3d4c0f4ccda139e18875
```  
or by cloning the repo at the above version tag and replacing the `extract.py`
file manually before installing via  
```bash
python wikiextractor/setup.py install
```  
Then call wikiextractor directly to extract the files  
```bash
python -m wikiextractor.WikiExtractor -b 1G --no-template wikidump/enwiki-20251101-pages-articles-multistream.xml.bz2 wikidump/text_notemplate
```

## Model Training

### Preprocessing

Install spacy model "en_core_web_md";
this is already included in the Dockerfile.  
```bash
python -m spacy download en_core_web_md
```

Preprocessing will take a great many hours to run.
While it would be best to incorporate multiprocessing,
`preprocess.py` processing only one file.
It would be best to run, as memory allows,
several instances of python, each
running on a different file.

Preprocess the files as below for each file:
```bash
python preprocess.py <file number in digits only>
```  

### Word2Vec Training

Training of the model, handled via  
```bash
python train_model.py
```  
takes substantially less time
(just over 3.5 hours on 31 of 32 cores of a
13th Gen Intel i9-13900HX processor).
