import csv
import requests

# rain data from .
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.html
# used dataset:
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.csv?precip%5B(2021-8-01T00:00:00Z):1:(2021-11-26T00:00:00Z)%5D%5B(30.0):.25:(42.0)%5D%5B(-123.0):.25:(-113.0)%5D

# return the latitude and longitude of a city using the url
def get_city_location(location_url) -> (float, float):
    response = requests.get(location_url)
    city_data = response.json()
    c_lat = float(city_data[0]["lat"]) # latitude of the city
    c_lon = float(city_data[0]["lon"]) # longitude of the city
    return c_lat, c_lon

# return a list of dates when a location is rainy, given the latitude, longitude, threshold of distance, threshold of rain, and the path of csv file
def rainy_days(file_path, dist_thresh, rain_thresh, c_lat, c_lon) -> list:
    dates = list()
    csv_file = open(file_path)
    csv_reader = csv.reader(csv_file, delimiter=',')

    # skip the header lines
    next(csv_reader, None) 
    next(csv_reader, None)
    
    for row in csv_reader:
        t, lat, lon, rain = row
        try: # process the row only when the numbers are valid
            rain = float(rain)
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            continue
        
        t = t[:10]
        lat_diff = abs(lat - c_lat)
        lon_diff = abs(lon - c_lon)
        if rain >= rain_thresh and lat_diff < dist_thresh and lon_diff < dist_thresh:
            dates.append((t, rain))
    csv_file.close()
    return dates

if __name__ == "__main__":
    city_name = str(input("Enter city name:[San Jose]") or "San Jose")
    location_url = "https://nominatim.openstreetmap.org/search.php?city=" + city_name  + "&format=jsonv2&namedetails=0&addressdetails=0&limit=1"
    file_path = "/data/chirps20GlobalPentadP05_233e_7ccc_b137.csv"
    dist_thresh = 0.05
    rain_thresh = 8.0

    c_lat, c_lon = get_city_location(location_url)
    dates = rainy_days(file_path, dist_thresh, rain_thresh, c_lat, c_lon)
    for item in dates:
        print(item)
    print("number of rainy 5-days:", len(dates))
