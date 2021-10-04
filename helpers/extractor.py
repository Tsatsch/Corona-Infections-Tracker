import urllib.request as request
import pandas as pd
from pathlib import Path
from helpers import data_parser


def download_rki(rki_excel_report_url):
    # fake user agent of Chrome to download blub excel
    fake_useragent = 'Chrome: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

    opener = request.build_opener()
    opener.addheaders = [('User-Agent', fake_useragent)]
    request.install_opener(opener)
    request.urlretrieve(rki_excel_report_url, "./resources/rki_report.xlsx")


def extract_data_from_rki(arr):
    arr = [x.lower() for x in arr]
    data_output = {}
    rki_report = Path("./resources/rki_report.xlsx")
    if not rki_report.is_file():
        raise FileNotFoundError("rki_report.xlsx NOT FOUND, download it first!")
    df = pd.read_excel('./resources/rki_report.xlsx', sheet_name=3)

    first_col = df.iloc[:, 0]
    requested_bundeslander = [item for item in data_parser.get_bundeslander() if item in arr]

    searched_rows = []
    for _, val in first_col.iteritems():
        if 'stand' in arr:
            if _ == 0:
                data_output['stand'] = val
        for blnd in requested_bundeslander:  # find bundeslander in excel and save their location
            if type(val) == str:
                if val.lower() == blnd:
                    searched_rows.append(_)

    for row_index in searched_rows:
        bundesland = df.iloc[row_index][0]
        aktuelle_inzidenz = df.iloc[row_index][-1]
        tendenz = aktuelle_inzidenz - df.iloc[row_index][-2]
        data_output[bundesland] = [round(aktuelle_inzidenz, 2), round(tendenz, 2)]

    return data_output