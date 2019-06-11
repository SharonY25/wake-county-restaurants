import pandas as pd
from src.yelp import fetch_yelp_data

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

restaurant = pd.read_csv('data/wake-county/Restaurants_in_Wake_County.csv')
violation = pd.read_csv('data/wake-county/Food_Inspection_Violations.csv')
inspection = pd.read_csv('data/wake-county/Food_Inspections.csv')

print(restaurant.head())
print(violation.head())
print(inspection.head())
