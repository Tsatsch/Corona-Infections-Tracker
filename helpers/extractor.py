import requests
from emoji import emojize


def extract_data_districts(base_url='https://api.corona-zahlen.org'):
    url = base_url + '/districts'
    keys_and_districts = {}  # {name : [key, week incidence, state, incidence compared to yesterday]}
    response = requests.request("GET", url).json()

    for key, value in response['data'].items():
        keys_and_districts[value['name']] = [key, round(value['weekIncidence'], 2), value['state']]
    return keys_and_districts


def extract_data_states(base_url='https://api.corona-zahlen.org'):
    url = base_url + '/states'
    keys_and_states = {}  # {name: [key, incidence]}
    response = requests.request("GET", url).json()
    for key, value in response['data'].items():
        keys_and_states[value['name']] = [key, value['weekIncidence']]
    return keys_and_states


def retrieve_from_data(name, data):
    text = ""
    for key, value in data.items():
        if key.lower() == name.lower():
            text += f'{key} - {str(round(float(value[1]), 2))}'
    if text == "":
        text = f'Uf... I could not find the location. Check if you have a typo in \"{name}\"'
    return text


def get_incidence_diff(name, data):
    base_url = "https://api.corona-zahlen.org"
    incidence = 0

    if len(data.keys()) == 16:
        for key, value in data.items():
            if key.lower() == name.lower():
                url = base_url + f'/states/{data[key][0]}/history/incidence/2'
                response = requests.request("GET", url).json()
                incidence = response['data'][data[key][0]]['history'][1]['weekIncidence'] - \
                            response['data'][data[key][0]]['history'][0]['weekIncidence']
    else:
        for key, value in data.items():
            if key.lower() == name.lower():
                url = base_url + f'/districts/{data[key][0]}/history/incidence/2'
                response = requests.request("GET", url).json()
                incidence = response['data'][data[key][0]]['history'][1]['weekIncidence'] - \
                            response['data'][data[key][0]]['history'][0]['weekIncidence']

    if incidence > 0:
        text = emojize(":arrow_upper_right:", use_aliases=True) + str(round(incidence, 2))
    else:
        text = emojize(":arrow_lower_left:", use_aliases=True) + str(round(incidence*-1, 2))

    return text
