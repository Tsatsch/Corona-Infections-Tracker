#!/bin/bash

url_rki=${URL_RKI}
token=${TOKEN}

echo exchange variables with real values
cat <<< $(jq ".url_rki = \"$url_rki\"" config.json) > config.json
cat <<< $(jq ".token = \"$token\"" config.json) > config.json
echo exchange finished

chmod +x main.py
python main.py