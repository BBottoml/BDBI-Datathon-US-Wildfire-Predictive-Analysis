from __future__ import print_function
from uszipcode import SearchEngine


def get_data_from_lat_long(latlong: tuple):
    """Return data pertaining to the specified latitude and longitude"""
    search = SearchEngine(simple_zipcode=True)
    result = search.by_coordinates(latlong[0], latlong[1], radius=30, returns=5)
    return result






if __name__ == "__main__":
    print(get_data_from_lat_long((41.850029, -87.650047)))
