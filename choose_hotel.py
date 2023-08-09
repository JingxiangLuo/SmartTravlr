import pandas as pd
import numpy as np
import sys
import math
import folium
from folium.plugins import HeatMap
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import scipy.stats as stats
from xml.dom.minidom import parse, parseString
import matplotlib.pyplot as plt
from math import cos, asin, sqrt, pi

def get_exif(filename):
    return Image.open(filename)._getexif()

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")
            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]
    return geotagging

def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0
    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds
    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    return (lat,lon)

def cal_distance(hotel, lat, lon):
    p = pi / 180
    lat1 = lat 
    lon1 = lon 
    lat2 = hotel['latitude']
    lon2 = hotel['longitude']
    a = 0.5-np.cos((lat2 - lat1) * p)/2 + np.cos(lat1 * p) * np.cos(lat2 * p) * (1 - np.cos((lon2 - lon1) * p)) / 2
    b = 12742*np.arcsin(np.sqrt(a))*1000
    return b

def choose_byDistance(hotel, dis):
    return hotel[hotel['distance'] < dis]

def choose_nearest(hotel):
    return hotel[hotel['distance'] == hotel['distance'].min()]

def choose_byRegion(hotel, region):
    return hotel[hotel['neighbourhood'] == region]

def choose_byReviews(hotel):
    return hotel[hotel['number_of_reviews'] == hotel['number_of_reviews'].max()]

def choose_byPrice(hotel, price):
    return hotel[hotel['price'] < price]

def choose_lowestPrice(hotel):
    return hotel[hotel['price'] == hotel['price'].min()]


def main(input_directory, output_directory):
    photo = input_directory
    exif = get_exif(photo)
    geotags = get_geotagging(exif)
    lat, lon = get_coordinates(geotags)
    hotel = pd.read_csv("listings.csv")
    hotel = hotel.drop(['host_id','neighbourhood_group','last_review','reviews_per_month','calculated_host_listings_count' ], axis = 1)
    distance = cal_distance(hotel, lat, lon)
    hotel['distance'] = distance
    
    hotel_filter = hotel_price = choose_byPrice(hotel, 100)
    hotel_filter = choose_byRegion(hotel_filter, 'Downtown')
    hotel_filter = choose_byDistance(hotel_filter, 20000)
    
    hotel_filter = choose_byReviews(hotel_filter)

    hotel_filter.to_csv(output_directory)
    
    
if __name__=='__main__':
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    main(input_directory,output_directory)
