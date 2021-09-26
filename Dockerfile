FROM python:3.9.7

ENV URL_MUC     url_muc
ENV URL_RKI     url_rki
ENV TOKEN       token

COPY requirements.txt .
COPY display.py .
COPY prepare_and_run.sh .
COPY config.json .

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y jq

RUN chmod +x prepare_and_run.sh
CMD ./prepare_and_run.sh