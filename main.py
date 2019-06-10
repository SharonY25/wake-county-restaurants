import pandas as pd
from src.yelp import fetch_yelp_data

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

restaurants = pd.read_csv('data/Restaurants_in_Wake_County.csv')
violations = pd.read_csv('data/Food_Inspection_Violations.csv')
inspections = pd.read_csv('data/Food_Inspections.csv')

fetch_yelp_data(restaurants)

print(restaurants.head())
print(violations.head())
print(inspections.head())
