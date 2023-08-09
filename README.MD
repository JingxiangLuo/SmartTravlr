# cmpt353-project
Repo of CMPT353 Final Project

# Libraries requirement (assuming you are running with Anaconda)
- pandas
- spark
- numpy
- scipy
- folium
- matplotlib
- math
- statsmodels.stats.weightstats


# problem1
1. Run code:
```
pyhton3 choose_hotel.py IMG_1435.JPG output.csv
```
Expected output:
- output.csv

2. Then run:
```
hotel_map.ipynb
```
Expect output: 
- data visualization

# problem2
Run code
```
pyhton3 have_a_trip.py
```
Then
- input latitude and longitude of start point
- input latitude and longitude of destination
- input n (number of output for each point)

Expected output:
- print n dataframes, each dataframe contain the coordinate,type, and name of the nearest.
- all.csv
- heatmap.html
- map.html


# problem3
1) open terminal with path to the "code" folder
2) running order:

        1 find_restaurant.ipynb
        expect output: get restaurant.csv (get the file from amenities-vancouver.json.gz)
        2 analyse_restaurant.ipynb
        expect output: data visualization
