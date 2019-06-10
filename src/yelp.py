import re
import requests
import os
import pandas as pd


yelp_phone_url = 'https://api.yelp.com/v3/businesses/search/phone?phone='


def fetch_yelp_data(restaurants):
    api_key = load_yelp_api_key()
    for ind in restaurants.index:
        hsisid = restaurants.iloc[ind]['HSISID']
        raw_phone_number = restaurants.iloc[ind]['PHONENUMBER']
        if not isinstance(raw_phone_number, str) or not raw_phone_number:
            print('Skipping restaurant with no phone number: ' + hsisid)
            continue

        print('Getting yelp data for ' + raw_phone_number)
        phone_number = format_phone_number(raw_phone_number)
        fetch_yelp_data_for(phone_number, hsisid, api_key)


def fetch_yelp_data_for(phone_number, hsisid, api_key):
    headers = {'Authorization': 'Bearer ' + api_key}
    url = yelp_phone_url + phone_number
    response = requests.get(url, headers=headers)
    print(response.json())


def format_phone_number(raw_phone_number):
    """
    Our data set has phone numbers that look like "(919) 666-6666"
    The Yelp API takes a phone number in the format "+19196666666"
    """
    numbers_only = re.sub(r'\D', '', raw_phone_number)
    if len(numbers_only) > 10
    numbers_only = numbers_only[0:10]

    return "+1" + numbers_only


def load_yelp_api_key():
    f = open('yelp_api_key')
    return f.read()


if __name__ == "__main__":
    fetch_yelp_data(pd.read_csv('Restaurants_in_Wake_County.csv'))
