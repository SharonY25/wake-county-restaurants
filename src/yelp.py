import re
import requests
import os
import pandas as pd
from yelp_categories import all_categories


yelp_phone_url = 'https://api.yelp.com/v3/businesses/search/phone?phone='


def fetch_yelp_data(restaurants):
    yelp_data = []  # This will be a list of dicts where each dict represents a row of data
    missing_yelp_data = []

    api_key = load_yelp_api_key()
    for ind in restaurants.index:
        hsisid = restaurants.iloc[ind]['HSISID']
        raw_phone_number = restaurants.iloc[ind]['PHONENUMBER']
        if not isinstance(raw_phone_number, str) or not raw_phone_number:
            # There is no phone number in the restaurants data so we can not look them up on Yelp.
            # Add an entry to the missing data and move on to the next restaurant.
            missing_yelp_data.append({
                'HSISID': hsisid,
                'REASON_MISSING': 'Phone number missing'
            })
            continue

        print('Getting yelp data for ' + raw_phone_number)
        phone_number = format_phone_number(raw_phone_number)

        search_results = fetch_yelp_data_for(phone_number, api_key)
        if search_results['total'] == 0:
            # There are no Yelp search results for that phone number.
            # Add an entry to the missing data and move on to the next restaurant
            missing_yelp_data.append({
                'HSISID': hsisid,
                'REASON_MISSING': 'No search results'
            })
            continue

        row = make_dataframe_entry(hsisid, phone_number, search_results)
        yelp_data.append(row)

    pd.DataFrame(yelp_data).to_csv('data/yelp/yelp.csv')
    pd.DataFrame(missing_yelp_data).to_csv('data/yelp/missing_yelp.csv')


def fetch_yelp_data_for(phone_number, api_key):
    """
    Send a GET request to the Yelp phone number search API
    Return the search results response as JSON
    """
    headers = {'Authorization': 'Bearer ' + api_key}
    url = yelp_phone_url + phone_number
    response = requests.get(url, headers=headers)
    return response.json()


def make_dataframe_entry(hsisid, phone_number, search_results):
    """
    The Yelp gives us search results in JSON format.  We need to convert this
    to a flat dict where the keys are the column names that we want.
    """
    if search_results['total'] > 1:
        print('Multiple search results for phone number ' +
              phone_number + ' (HSISID ' + str(hsisid) + ')')
        print('Using the first result for now - investigate this later.')
        print(search_results)

    business = search_results['businesses'][0]
    row = {
        'HSISID': hsisid,
        'YELP_ID': business.get('id', ''),
        'ALIAS': business.get('alias', ''),
        'YELP_NAME': business.get('name', ''),
        'JSON_URL': yelp_phone_url + phone_number,
        'NUMBER_OF_REVIEWS': business.get('review_count', 0),
        'RATING': business.get('rating', 0),
        'PRICE': len(business.get('price', '$')),
        'HAS_DELIVERY': 1 if 'delivery' in business.get('transactions', []) else 0,
        'HAS_PICKUP': 1 if 'pickup' in business.get('transactions', []) else 0,
        'HAS_ONLINE_RESERVATION': 1 if 'restaurant_reservation' in business.get('transactions', []) else 0
    }

    # Add one column for each of Yelp's restaurant categories
    for category_name in all_categories:
        cat_column = make_column_name_for_category(category_name)
        for category in business['categories']:
            if category['title'] == category_name:
                row[cat_column] = 1
                break
            row[cat_column] = 0

    return row


def make_column_name_for_category(category):
    """
    Yelp category names look like "American (New)" or "Breakfast & Brunch"
    We would like column names like "HAS_CATEGORY_AmericanNew" or "HAS_CATEGORY_BreakfastBrunch"
    """
    return 'HAS_CATEGORY_' + re.sub(r'[^A-Za-z0-9]', '', category)


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
    """
    When you're making a request programmatically (i.e. not from a browser), Yelp does not let
    unauthenticated traffic access its API.  We need to have an API key saved in the root directory
    of the project, and include this key in all of our requests.
    """
    f = open('yelp_api_key')
    return f.read()


if __name__ == "__main__":
    fetch_yelp_data(pd.read_csv(
        'data/wake-county/Restaurants_in_Wake_County.csv'))
