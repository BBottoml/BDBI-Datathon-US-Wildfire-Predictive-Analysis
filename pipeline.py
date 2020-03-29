from __future__ import print_function
from uszipcode import SearchEngine
import pandas as pd 
import json
import requests
import operator
import csv


def get_data_from_lat_long(latlong: tuple):
    """Return data pertaining to the specified latitude and longitude"""
    search = SearchEngine(simple_zipcode=False)
    result = search.by_coordinates(latlong[0], latlong[1], radius=30, returns=1)
    if result != [] and result != None:
        return result[0].to_dict()

# Data gathering functions 

def get_population_density(raw_data: dict):
    """Return the population density for a given region"""
    return raw_data["population_density"]

def get_median_home_value(raw_data: dict):
    """Return the median home value for a given region"""
    return raw_data["median_home_value"]

def get_median_household_income(raw_data: dict):
    """Return the median household income"""
    return raw_data["median_household_income"]

def get_number_housing_units(raw_data: dict):
    """Return the number of housing units in the region""" 
    return raw_data["housing_units"]

def get_number_occupied_housing_units(raw_data: dict):
    """Return the number of occupied housing units"""
    return raw_data["occupied_housing_units"]

def get_house_age_breakdown(raw_data: dict):
    """Return a dictionary representing decades in which houses were built"""
    ages_raw = raw_data["year_housing_was_built"][0]["values"]
    ages = {1930: 0, 1940: 0, 1950: 0, 1960: 0, 1970: 0, 1980: 0, 1990: 0, 2000: 0, 2010: 0} 

    return transform_dict(ages_raw, ages)

def get_degree_breakdown(raw_data: dict):
    """Return a dictionary representing the number of degree holders"""
    degree_raw = raw_data["educational_attainment_for_population_25_and_over"][0]["values"]
    degrees = {"NO_HS": 0, "HS": 0, "Associates": 0, "Bachelors": 0, "Masters": 0, "Professional": 0, "Doctorate": 0} 

    return transform_dict(degree_raw, degrees)

def get_earnings_breakdown(raw_data: dict):
    """Return a dictionary representing earnings breakdown"""
    earnings_raw = raw_data["source_of_earnings"][0]["values"]
    earnings = {"None": 0, "Part_Time": 0, "Full_Time": 0} 
    
    return transform_dict(earnings_raw, earnings)

# Helper functions

def get_majority_value(data_dict: dict):
    max_val = -1
    majority = None
    for key, value in data_dict.items():
        if value > max_val:
            max_val = value 
            majority = key

    return majority

def transform_dict(raw_dict, new_dict):
    i = 0
    for key in new_dict.keys():
        new_dict[key] = raw_dict[i]["y"]
        i += 1
    
    return new_dict

def verify_data(raw_data: dict):
    """Will verify that raw_data is populated with the necessary fields to perform analysis"""
    try:
        get_median_household_income(raw_data)
        get_median_home_value(raw_data)
        get_population_density(raw_data)
        get_number_housing_units(raw_data)
    except: 
        return -1


    return 0

def construct_dataframe(latlong_list: list):
    raw_data_col = [] 
    income_col = [] 
    home_val_col = []
    pop_density_col = [] 
    housing_num_unit_col = [] 

    for latlong in latlong_list:
        raw_data_col.append(latlong)
        income_col.append(get_median_household_income(latlong))
        home_val_col.append(get_median_home_value(latlong))
        pop_density_col.append(get_population_density(latlong))
        housing_num_unit_col.append(get_population_density(latlong))
    
    d = {'raw_data': raw_data_col, 'median_household_income': income_col, 'median_home_value': home_val_col, 'population_density': pop_density_col, 'number_housing_units': housing_num_unit_col}
    return pd.DataFrame(data=d)


# temporary name 
def model_algorithm(data_frame):
    pass


if __name__ == "__main__":
    #raw_data = (get_data_from_lat_long((33.3062856, -111.8673082))[0]).to_dict()
    print("="*50)
    print("Wildfire Pipeline Predictive Analysis Program")
    print("="*50)
    print("Gathering data...")
    
    latlongs = {}  # map lat long tuple to raw data dictionary 
    '''
    0 key: (lat, long, confidence) -> value: {DICT} 
    1   
    2
    3
    4
    5
    6
    7
    ...
    N 
    '''

    ''' 
    Row: (lat, long, confidence): get_median_household_income(raw_data), get_median_home_value(raw_data)
    '''

    latlong_severity = {} # map lat long tuple to score determined by model

    # GET request to NASA active fire data source
    req = requests.get(r'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_7d.csv')
    if req.status_code != 200:
        exit(1)

    with open('current_data.csv', 'w') as f:
        writer = csv.writer(f)
        for line in req.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))
    
    data = pd.read_csv('current_data.csv')
    
    # acquire data for each potential wildfire 
    data['latlongtuple'] = list(zip(data.latitude, data.longitude, data.confidence))
    i = 0
    for item in data['latlongtuple']:
        if (item[2] > 90): # determine if confidence is greater than 95 
            latlongs[item] = get_data_from_lat_long((item[0], item[1]))
            i+=1
    
    print("="*50)
    print("Done gathering data...")
    print(i, "potential wildfires identified")
    
    # verify each of the potential wildfires
    latlong_list = []
    suitable = 0
    for key,value in latlongs.items():
        if verify_data(value) != -1:
            latlong_list.append(value)
            suitable+=1
    print(suitable, "wildfires suitable for analysis")
    print("="*50)

    #print(len(latlong_list))
    df = construct_dataframe(latlong_list)
    print(df) 

    # TODO: Call model_algorithm on the data frame, df 
    # model_algorithm(df)

    # Create model and determine severity for each potential wildfire 
    # Sort by most severe and display
    #latlong_severity = sorted(latlong_severity.items(), key=operator.itemgetter(1), reverse=True)
    #print(len(latlong_severity))
    '''
    #with open('sample_data.json', 'w', encoding='utf-8') as f:
    #    json.dump(raw_data, f, ensure_ascii=False, indent=4)
    with open("sample_data.json", "r") as read_file:
        data = json.load(read_file)
    
    print(get_earnings_breakdown(data))
    '''