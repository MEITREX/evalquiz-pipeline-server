FROM python:3.10.11-slim-buster

WORKDIR /evalquiz-pipeline-server
COPY requirements.txt requirements.txt

RUN pip3 install betterproto[compiler]==2.0.0b6
RUN pip3 install grpcio
RUN pip3 install grpcio-tools
RUN pip3 install grpclib
RUN pip3 install blake3
RUN pip3 install pytest
RUN pip3 install pytest-asyncio
RUN pip3 install filetype
RUN pip3 install mypy
RUN pip3 install pyflakes
RUN pip3 install black
RUN pip3 install jsonpickle
RUN pip3 install sphinx
RUN pip3 install sphinx_rtd_theme
RUN pip3 install pymongo
RUN pip3 install gensim
RUN pip3 install nltk
RUN pip3 install tiktoken
RUN pip3 install openai
RUN pip3 install pptx2md
RUN pip3 install pypandoc_binary
RUN pip3 install datasets