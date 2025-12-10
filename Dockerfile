FROM ubuntu:24.04
RUN apt update 
RUN apt install -y --no-install-recommends \
        bash git wget \
        python3 python3-pip python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . .
RUN mkdir model -p wikidump/processed wikidump/text_notemplate
RUN python3 -m venv .venv && \
    ./.venv/bin/python -m pip install pip setuptools -U && \
    ./.venv/bin/python -m pip install -r requirements.txt && \
    ./.venv/bin/python -m pip install git+https://github.com/attardi/wikiextractor.git@ab8988ebfa9e4557411f3d4c0f4ccda139e18875
ENV PATH="/.venv/bin:$PATH"
CMD ["bash"]
