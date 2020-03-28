from __future__ import print_function
from uszipcode import SearchEngine
import json


def get_data_from_lat_long(latlong: tuple):
    """Return data pertaining to the specified latitude and longitude"""
    search = SearchEngine(simple_zipcode=False)
    result = search.by_coordinates(latlong[0], latlong[1], radius=30, returns=1)
    return result

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

def get_majoriy_house_age(raw_data: dict):
    """Return the year in which the majority of houses were built"""
    house_ages = raw_data["year_housing_was_built"][0]["values"]
    years = {1930: 0, 1940: 0, 1950: 0, 1960: 0, 1970: 0, 1980: 0, 1990: 0, 2000: 0, 2010: 0} 

    i = 0
    for key in years.keys():
        years[key] = house_ages[i]["y"]
        i += 1
    
    return get_majority_value(years)

def get_majority_value(data_dict: dict):
    max_val = -1
    majority = None
    for key, value in data_dict.items():
        if value > max_val:
            max_val = value 
            majority = key

    return majority
    

if __name__ == "__main__":
    #raw_data = (get_data_from_lat_long((33.3062856, -111.8673082))[0]).to_dict()
   
    #with open('sample_data.json', 'w', encoding='utf-8') as f:
    #    json.dump(raw_data, f, ensure_ascii=False, indent=4)
    with open("sample_data.json", "r") as read_file:
        data = json.load(read_file)
    
    print(get_majoriy_house_age(data))