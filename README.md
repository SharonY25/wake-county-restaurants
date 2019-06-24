# wake-county-restaurants

A data science project analyzing sanitation scores for Wake County restaurants

## Setup

1. Clone the repository

    ```
    git clone git@github.com:SharonY25/wake-county-restaurants.git
    cd wake-county-restaurants
    ```

2. If you need to keep your python environments isolated, set up a virtual environment

    ```
    virtualenv $(which python3) venv
    source venv/bin/activate
    pip install -r requirements.txt
    ````

    And when you're finished working in this environment,

    ```
    deactivate
    ```

3. Download the raw input data

    One of our raw data files is larger than GitHub's per-file limit (100MB),
    so we do not track our raw data in git.

    From [Wake County Data](http://data-ral.opendata.arcgis.com/datasets/Wake::food-inspections), download:

    - Restaurants_in_Wake_County.csv
    - Food_Inspections.csv
    - Food_Inspection_Violations.csv

    to `wake-county-restaurants/data`

## Running the project

To run the main data analysis module, run

```
python main.py
```

To download and save data from Yelp, first you need to get an API key from
[Yelp](https://www.yelp.com/developers/documentation/v3/authentication), and save
it in a plain text file `wake-county-restaurants/yelp_api_key`.
Then, run

```
python src/yelp.py
```

## About the data

TODO