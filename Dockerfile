FROM python:3.9.7
ENV PYTHONUNBUFFERED=1

ENV URL_RKI     url_rki
ENV TOKEN       token

COPY requirements.txt .
COPY helpers ./helpers
COPY resources ./resources
COPY main.py .
COPY prepare_and_run.sh .
COPY config.json .

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y jq

RUN chmod +x prepare_and_run.sh
CMD ./prepare_and_run.sh