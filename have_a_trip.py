#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import folium
import sys

#Ref
#https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
def distance(place,lat2,lon2):
    e=6371
    lat = lat2
    lon = lon2
    STlat=place['lat']
    STlon=place['lon']
    dlat=np.deg2rad(np.fabs(STlat-lat))
    dlon=np.deg2rad(np.fabs(STlon-lon))
    a=np.sin(dlat/2)*np.sin(dlat/2)+np.cos(np.deg2rad(lat))*np.cos(np.deg2rad(STlat))*np.sin(dlon/2)*np.sin(dlon/2)
    c=np.arcsin(np.sqrt(a))*2
    return c*e


#remove unnecessary column, remove any rows with null, groupby the data to figure out how many kinds of amenities in Vancouver, sort it and list all kinds of amenities in a csv file
def listall(amenities):
    amenities = amenities.drop(['timestamp', 'tags'], axis=1)
    amenities = amenities.dropna(axis=0)
    a=amenities.groupby('amenity').count()
    a=a.sort_values(['name'], ascending=False)
    a.to_csv('all.csv')

#remove all the data we are not interested in,remove all rows with null,remove unnecessary column, return a cleaned dataframe.
def clean(amenities):
    cleaned=amenities[(amenities['amenity'] =='restaurant') | (amenities['amenity'] =='fast_food')| (amenities['amenity'] =='cafe')| (amenities['amenity'] =='pub')| (amenities['amenity'] =='bar')| (amenities['amenity'] =='place_of_worship')| (amenities['amenity'] =='ice_cream')| (amenities['amenity'] =='school')| (amenities['amenity'] =='community_centre')| (amenities['amenity'] =='library')| (amenities['amenity'] =='theatre')| (amenities['amenity'] =='public_bookcase')| (amenities['amenity'] =='ferry_terminal')| (amenities['amenity'] =='bureau_de_change')| (amenities['amenity'] =='marketplace')| (amenities['amenity'] =='dojo')| (amenities['amenity'] =='social_centre')| (amenities['amenity'] =='nightclub')| (amenities['amenity'] =='cinema')| (amenities['amenity'] =='arts_centre')| (amenities['amenity'] =='events_venue')| (amenities['amenity'] =='university')| (amenities['amenity'] =='food_court')| (amenities['amenity'] =='spa')| (amenities['amenity'] =='clock')|(amenities['amenity'] =='lounge')|(amenities['amenity'] =='casino')|(amenities['amenity'] =='chiropractor')|(amenities['amenity'] =='bistro')|(amenities['amenity'] =='monastery')|(amenities['amenity'] =='leisure')|(amenities['amenity'] =='park')|(amenities['amenity'] =='gambling')]
    cleaned=cleaned.reset_index()
    cleaned=cleaned.drop(['index'],axis=1)
    cleaned = cleaned.drop(['timestamp', 'tags'], axis=1)
    cleaned = cleaned.dropna(axis=0)
    cleaned=cleaned[cleaned['lon']>-123.4473026066329]#remove data outside of metro Vancouver
    cleaned=cleaned[cleaned['lon']<-122.462472]
    return cleaned


def heatmap(data):
    from folium.plugins import HeatMap
    san_map1 = folium.Map(location = [49.233292,-123.156132], zoom_start = 10)
    heatdata = data[['lat','lon']].values.tolist()
    HeatMap(heatdata,radius=10).add_to(san_map1)
    san_map1.save("heatmap.html")

#user input the starting point coordinate, destination coordinate and the number of amenities want to display for each point
def inputdata(amenities):
    maxlat=amenities['lat'].max()#49.4598489
    minlat=amenities['lat'].min()#49.0053233
    maxlon=amenities['lon'].max()#-122.0016829
    minlon=amenities['lon'].min()#-123.4772643
    while True:
        try:
            templat=float(input('Enter Startpoint Latitude:'))
        except ValueError:
            print("Sorry, I didn't understand that.") #the input have to be a float
            continue
        else:
            if templat <maxlat and templat>minlat: #the input coordinate should in Metro Vancouver
                start_lat=templat
            else:
                print("Sorry, it is outside of Metro Vancouver")
                print("range:49.0053233<lat<49.4598489")
                continue
            break
        
    while True:
        try:
            templon=float(input('Enter Startpoint Longitude:'))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            if templon <maxlon and templon>minlon: 
                start_lon=templon
            else:
                print("Sorry, it is outside of Metro Vancouver")
                print("range:-123.4772643<lon<-122.0016829")
                continue
            break

    while True:
        try:
            templat2=float(input('Enter Destination Latitude:'))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            if templat2 <maxlat and templat2>minlat: 
                dest_lat=templat2
            else:
                print("Sorry, it is outside of Metro Vancouver")
                print("range:49.0053233<lat<49.4598489")
                continue
            break

    while True:
        try:
            templon2=float(input('Enter Destination Longitude:'))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        else:
            if templon2 <maxlon and templon2>minlon: 
                dest_lon=templon2
            else:
                print("Sorry, it is outside of Metro Vancouver")
                print("range:-123.4772643<lon<-122.0016829")
                continue
            break
    while True:
        try:
            number=int(input('Enter Number of Amenities:'))
        except ValueError:
            print("Sorry, I didn't understand that. Type a integer and try again")
            continue
        else:
            if number >0: 
                n=number
            else:
                print("Sorry,Number of Amenities have to greater than 0")
                continue
            break
    return start_lat,start_lon,dest_lat,dest_lon,n


#calculate the distance from amenities to starting point,25%-traveled point,50%-traveled point,75%-traveled point,destination point(in km)
#return the dataframe with calculated distance for each point
def FivePointTrip(cleaned,x,y,xx,yy):
    d = {'lat': x, 'lon': y}
    df=pd.DataFrame(data=d,index=[0])
    s = {'lat': xx, 'lon': yy}
    dest = pd.DataFrame(data=s,index=[0])
    latdiff=xx-x
    londiff=yy-y
    #first point
    temp=cleaned.copy()
    temp['lon2']=df['lon'].iloc[0]
    temp['lat2']=df['lat'].iloc[0]
    temp['start']=distance(temp,temp['lat2'],temp['lon2']) #calculate distance in km
    temp=temp.drop(['lon2','lat2'],axis=1)
    #25% traveled
    df2=df.copy()
    df2['lat']=df['lat']+(latdiff/4)
    df2['lon']=df['lon']+(londiff/4)
    temp2=cleaned.copy()
    temp2['lon2']=df2['lon'].iloc[0]
    temp2['lat2']=df2['lat'].iloc[0]
    temp2['25%']=distance(temp2,temp2['lat2'],temp2['lon2'])
    temp2=temp2.drop(['lon2','lat2'],axis=1)
    #50% traveled
    df3=df2.copy()
    df3['lat']=df2['lat']+latdiff/4
    df3['lon']=df2['lon']+londiff/4
    temp3=cleaned.copy()
    temp3['lon2']=df3['lon'].iloc[0]
    temp3['lat2']=df3['lat'].iloc[0]
    temp3['50%']=distance(temp3,temp3['lat2'],temp3['lon2'])
    temp3=temp3.drop(['lon2','lat2'],axis=1)
    #75% traveled.
    df4=df3.copy()
    df4['lat']=df3['lat']+latdiff/4
    df4['lon']=df3['lon']+londiff/4
    temp4=cleaned.copy()
    temp4['lon2']=df4['lon'].iloc[0]
    temp4['lat2']=df4['lat'].iloc[0]
    temp4['75%']=distance(temp4,temp4['lat2'],temp4['lon2'])
    temp4=temp4.drop(['lon2','lat2'],axis=1)
    #destination
    df5=df4.copy()
    df5['lat']=df4['lat']+latdiff/4
    df5['lon']=df4['lon']+londiff/4
    temp5=cleaned.copy()
    temp5['lon2']=df5['lon'].iloc[0]
    temp5['lat2']=df5['lat'].iloc[0]
    temp5['dest']=distance(temp5,temp5['lat2'],temp5['lon2'])
    temp5=temp5.drop(['lon2','lat2'],axis=1)
    return temp,temp2,temp3,temp4,temp5

def printKnearest(n,temp,temp2,temp3,temp4,temp5):
    #print n nearest amenities
    print(temp.nsmallest(n, 'start', keep='all'),'\n')
    print(temp2.nsmallest(n, '25%', keep='all'),'\n')
    print(temp3.nsmallest(n, '50%', keep='all'),'\n')
    print(temp4.nsmallest(n, '75%', keep='all'),'\n')
    print(temp5.nsmallest(n, 'dest', keep='all'),'\n')



#Ref https://python-visualization.github.io/folium/modules.html?highlight=marker
#make a map, all amenities are labeled with blue mark, starting point and destination are labeled with orange point
def makemap(n,x,y,xx,yy,temp,temp2,temp3,temp4,temp5):
    san_map = folium.Map(location=[49.233292,-123.156132], zoom_start=10)
    
    latitudes = (x,xx)
    longitudes = (y,yy)
    incidents = folium.map.FeatureGroup()
    for lat, lng, in zip(latitudes, longitudes):
        incidents.add_child(
            folium.CircleMarker(
                [lat, lng],
                radius=5,
                color='orange',
                fill=True,
                fill_color='orange',
                fill_opacity=1
            )
        )
    san_map.add_child(incidents)
    
    latitudes = list(temp.nsmallest(n, 'start', keep='all')['lat'])
    longitudes = list(temp.nsmallest(n, 'start', keep='all')['lon'])
    labels = list(temp.nsmallest(n, 'start', keep='all')['name'])
    for lat, lng, label in zip(latitudes, longitudes, labels):
        folium.Marker([lat, lng]).add_to(san_map)
        
    latitudes = list(temp2.nsmallest(n, '25%', keep='all')['lat'])
    longitudes = list(temp2.nsmallest(n, '25%', keep='all')['lon'])
    labels = list(temp2.nsmallest(n, '25%', keep='all')['name'])

    for lat, lng, label in zip(latitudes, longitudes, labels):
        folium.Marker([lat, lng], popup=label).add_to(san_map) 

    latitudes = list(temp3.nsmallest(n, '50%', keep='all')['lat'])
    longitudes = list(temp3.nsmallest(n, '50%', keep='all')['lon'])
    labels = list(temp3.nsmallest(n, '50%', keep='all')['name'])
    
    for lat, lng, label in zip(latitudes, longitudes, labels):
        folium.Marker([lat, lng], popup=label).add_to(san_map) 

    latitudes = list(temp4.nsmallest(n, '75%', keep='all')['lat'])
    longitudes = list(temp4.nsmallest(n, '75%', keep='all')['lon'])
    labels = list(temp4.nsmallest(n, '75%', keep='all')['name'])

    for lat, lng, label in zip(latitudes, longitudes, labels):
        folium.Marker([lat, lng], popup=label).add_to(san_map)    
    
    latitudes = list(temp5.nsmallest(n, 'dest', keep='all')['lat'])
    longitudes = list(temp5.nsmallest(n, 'dest', keep='all')['lon'])
    labels = list(temp5.nsmallest(n, 'dest', keep='all')['name'])

    for lat, lng, label in zip(latitudes, longitudes, labels):
        folium.Marker([lat, lng], popup=label).add_to(san_map)    

    san_map.save("map.html")

def main():

    amenities = pd.read_json('amenities-vancouver.json.gz', lines=True) #read data
    listall(amenities) #output the groupbyed,sorted data for analysis
    data=pd.read_json('amenities-vancouver.json.gz', lines=True) #read all data
    cleaned=clean(data) # clean data according to the list of interested data
    heatmap(cleaned)
    (start_lat,start_lon,dest_lat,dest_lon,n_intersted)=inputdata(amenities) # input coordinate of start point and destination,number of amenities we want to display
    (point1,point2,point3,point4,point5)=FivePointTrip(cleaned,start_lat,start_lon,dest_lat,dest_lon)# calculate distance between each point and amenities
    printKnearest(n_intersted,point1,point2,point3,point4,point5) # print n nearest amenities from each point
    makemap(n_intersted,start_lat,start_lon,dest_lat,dest_lon,point1,point2,point3,point4,point5) # make a map with folium


if __name__ == '__main__':
    main()
