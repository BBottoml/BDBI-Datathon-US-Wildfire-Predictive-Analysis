from __future__ import print_function
from uszipcode import SearchEngine
from region import Region
import json

def get_data_from_lat_long(latlong: tuple):
    """Return data pertaining to the specified latitude and longitude"""
    search = SearchEngine(simple_zipcode=False)
    result = search.by_coordinates(latlong[0], latlong[1], radius=30, returns=1)
    return result


if __name__ == "__main__":
    raw_data = (get_data_from_lat_long((41.850029, -87.650047))[0]).to_dict()
   
    with open('sample_data.json', 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=4)

    region = Region(raw_data) 
    print(region.raw_data)