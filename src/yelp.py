import re
import requests
import os
import pandas as pd


yelp_phone_url = 'https://api.yelp.com/v3/businesses/search/phone?phone='


def fetch_yelp_data(restaurants):
    yelp_data = []
    missing_yelp_data = []

    temp = 0

    api_key = load_yelp_api_key()
    for ind in restaurants.index:
        hsisid = restaurants.iloc[ind]['HSISID']
        raw_phone_number = restaurants.iloc[ind]['PHONENUMBER']
        if not isinstance(raw_phone_number, str) or not raw_phone_number:
            missing_yelp_data.append({
                'HSISID': hsisid,
                'REASON_MISSING': 'Phone number missing'
            })
            continue

        print('Getting yelp data for ' + raw_phone_number)
        phone_number = format_phone_number(raw_phone_number)

        search_results = fetch_yelp_data_for(hsisid, phone_number, api_key)
        if search_results['total'] == 0:
            missing_yelp_data.append({
                'HSISID': hsisid,
                'REASON_MISSING': 'No search results'
            })
            continue

        row = make_dataframe_entry(hsisid, phone_number, search_results)
        yelp_data.append(row)

        temp += 1
        if temp > 100:
            break

    pd.DataFrame(yelp_data).to_csv('data/yelp/yelp.csv')
    pd.DataFrame(missing_yelp_data).to_csv('data/yelp/missing_yelp.csv')


def fetch_yelp_data_for(hsisid, phone_number, api_key):
    headers = {'Authorization': 'Bearer ' + api_key}
    url = yelp_phone_url + phone_number
    response = requests.get(url, headers=headers)
    return response.json()


def make_dataframe_entry(hsisid, phone_number, search_results):
    if search_results['total'] > 1:
        print('Multiple search results for phone number ' +
              phone_number + ' (HSISID ' + str(hsisid) + ')')
        print('Using the first result for now - investigate this later.')

    business = search_results['businesses'][0]
    return {
        'HSISID': hsisid,
        'YELP_ID': business['id'],
        'ALIAS': business['alias'],
        'YELP_NAME': business['name'],
        'JSON_URL': yelp_phone_url + phone_number
    }


def format_phone_number(raw_phone_number):
    """
    Our data set has phone numbers that look like "(919) 666-6666"
    The Yelp API takes a phone number in the format "+19196666666"
    """
    numbers_only = re.sub(r'\D', '', raw_phone_number)
    if len(numbers_only) > 10:
        numbers_only = numbers_only[0:10]

    return "+1" + numbers_only


def load_yelp_api_key():
    f = open('yelp_api_key')
    return f.read()


if __name__ == "__main__":
    fetch_yelp_data(pd.read_csv(
        'data/wake-county/Restaurants_in_Wake_County.csv'))
