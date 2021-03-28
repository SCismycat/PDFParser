FROM python:3.6.5-slim
LABEL MAINTAINER="lifei@plantdata.cn"


WORKDIR /work

COPY ./requirements.txt /work/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -i https://pypi.douban.com/simple --no-cache-dir -r /work/requirements.txt

ENV PYTHONPATH=/usr/local/lib/python3.6/site-packages
COPY ./src /work/src
COPY ./test /work/test
COPY ./utils /work/utils

ENTRYPOINT ["python", "/work/src/main.py"]
