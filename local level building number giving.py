#!/usr/bin/env python
# coding: utf-8

# In[10]:


import geopandas as gpd
import matplotlib.pyplot as plt


# In[11]:


buildings=gpd.read_file("C:\\sample\\buildings\\buildings.shp")
buildings.to_crs('EPSG:4326',inplace=True)


# In[12]:


amities=gpd.read_file("C:\\sample\\aminities\\aminities.shp")
amities.to_crs('EPSG:4326',inplace=True)


# In[13]:


fig,ax=plt.subplots(figsize=(16,9))
buildings.plot(ax=ax)
amities.plot(color='red',ax=ax)


# In[14]:


amities.head()


# In[15]:


amities=amities[['amenity','name','geometry']]


# 

# In[16]:


amities=amities.dropna()


# In[17]:


fig,ax=plt.subplots(figsize=(16,9))
buildings.plot(ax=ax)
amities.plot(color='red',ax=ax)


# In[18]:


amities['centroid']=amities.centroid


# In[19]:


amities.set_geometry(amities['centroid'],inplace=True)


# In[20]:


amities.drop(columns=['centroid'],inplace=True)


# In[21]:


amities=gpd.read_file("C:\\sample\\aminities\\filtered\\amities_filtered.shp")


# In[22]:


amities.loc[1,'name']='Wasinkhyah Bahi Baha'


# In[23]:


amities.crs


# In[24]:


buildings['centroid']=buildings.centroid


# In[25]:


buildings.set_geometry(buildings['centroid'],inplace=True)


# In[26]:


buildings.columns


# In[27]:


buildings=buildings[['geometry']]


# In[28]:


amities['name']=amities['name']+" "+amities['amenity']


# In[29]:


amities


# In[30]:


buildings=buildings.to_crs(3857)
amities=amities.to_crs(3857)
buildings=buildings.reindex()
amities=amities.reindex()
distance_dict={}
for index_b,value_b in enumerate(buildings['geometry']):
        distance_value={}
        for index,value in enumerate(amities['geometry']):
            distance=value_b.distance(value)
            distance_value[amities.loc[index,'name']]=distance
        distance_dict[index_b]=distance_value


# In[31]:


amities


# In[32]:


distance_dict


# In[ ]:





# In[33]:


# calculating distances from each amities and sorting
# buildings=buildings.to_crs(3857)
# amities=amities.to_crs(3857)
buildings=buildings.reindex()
amities=amities.reindex()
distance_dict={}
for index_b,value_b in enumerate(buildings['geometry']):
        distance_value={}
        for index,value in enumerate(amities['geometry']):
            distance=value_b.distance(value)
            distance_value[amities.loc[index,'name']]=int(round(distance,0))
        distance_dict[index_b]=distance_value
buildings_distances_sorted={}
for build in distance_dict.keys():
    newlist=list(distance_dict[build].values())
    newlist.sort()
    storted_distance_index={}
    for i in newlist[:3]:
        for j in distance_dict[build].keys():
            if i==distance_dict[build][j]:
                storted_distance_index[j]=i
    buildings_distances_sorted[build]=storted_distance_index


# In[ ]:





# In[34]:


buildings_names=[]
selected_amities=[]
distances=[]
for index,value in enumerate(buildings_distances_sorted.keys()):
    building=buildings.loc[index,'geometry']
    for j in buildings_distances_sorted[index].keys():
        selected_amities.append(j)
        distances.append(buildings_distances_sorted[index][j])
        buildings_names.append(building)


# In[35]:


df_after=gpd.GeoDataFrame({'geometry':buildings_names,'amities':selected_amities,'distance':distances},crs=3857)


# In[ ]:





# In[37]:


def calculate_degree(point1,point2):
    x1=point1.x
    y1=point1.y
    x2=point2.x
    y2=point2.y
    del_e=(x2-x1)
    del_n=(y2-y1)
    degree=math.degrees(math.atan(abs((x2-x1)/(y2-y1))))
    print(del_e,del_n)
    if del_e>=0 and del_n>=0:
        return degree
    if del_e>=0 and del_n<0:
        return 180-degree
    if del_e<0 and del_n<0:
        return 180+degree
    if del_e<0 and del_n>=0:
        return 360-degree


# In[44]:


import math
def calculate_direction(point1,point2):
    degree=calculate_degree(point1,point2)
    print(degree)
    if degree>22.5 and degree<=67.5:
        return 'NE'
    if degree>67.5 and degree<=112.5:
        return 'E'
    if degree>112.5 and degree<=157.5:
        return 'SE'
    if degree>157.5 and degree<=202.5:
        return 'S'
    if degree>202.5 and degree<=247.5:
        return 'SW'
    if degree>247.5 and degree<=292.5:
        return 'W'
    if degree>292.5 and degree<=337.5:
        return 'NW'
    if (degree>337.5 and degree<=360) or (degree>=0 or degree<=22.5):
        return 'N'
    else:
        return 'N/A'


# In[45]:


import shapely


# In[46]:


shapely.Point()


# In[ ]:





# In[47]:


calculate_direction(list(amities[amities['name']=='Banepa Hospital hospital']['geometry'])[0],list(amities[amities['name']=='Shikshya Sadan H.S.S school']['geometry'])[0])


# In[ ]:





# In[48]:


for i in list(df_after.index):
    amities_name=df_after.loc[i,'amities']
    amities_geom=list(amities[amities['name']==amities_name]['geometry'])[0]
    df_after.loc[i,'amities_geom']=amities_geom


# In[49]:


df_after


# In[50]:


amities


# In[51]:


amitie_geom=list(amities[amities['name']==df_after['amities'][0]]['geometry'])[0]


# In[52]:


buildings['geometry'][0].x


# In[53]:


direction_list=[]
for building,amitie in zip(list(df_after['geometry']),list(df_after['amities_geom'])):
    direction=calculate_direction(amitie,building)
    print(amitie_geom,building,direction)
    direction_list.append(direction)
    print("-------------")


# In[ ]:





# In[54]:


df_after['direction']=direction_list


# In[55]:


df_after


# In[56]:


len(df_after['geometry'].unique())


# In[57]:


mapping_building={}
new_list=[i for i in range(len(df_after['geometry'].unique()))]
for i,j in zip(df_after['geometry'].unique(),new_list):
    mapping_building[i]=j+1


# In[58]:


len(list(mapping_building.keys()))


# In[59]:


df_after['building_id']=df_after['geometry']


# In[60]:


df_after_copy=df_after.copy()


# In[61]:


df_after['building_id']=df_after['building_id'].map(mapping_building)


# In[ ]:





# In[62]:


newdict={}
for j in df_after['building_id'].unique():
    code_names=[]
    for i in df_after[df_after['building_id']==j].index:
        amities_name=df_after.loc[i,'amities']
        distance=df_after.loc[i,'distance']
        direction=df_after.loc[i,'direction']
        code=f"{amities_name},{distance},{direction}"
        code_names.append(code)
    point=list(df_after[df_after['building_id']==j]['geometry'])[0]
    newdict[point]=code_names


# In[63]:


newdict


# In[64]:


newvalues={}
for i in newdict.keys():
    code=str()
    for index,value in enumerate(newdict[i][:2]):
        if index==0:
            code=value
        else:
            code=code+"--"+value
    newvalues[i]=code


# In[65]:


new_final_dict={'geometry':newvalues.keys(),'name':newvalues.values()}


# In[66]:


final_df=gpd.GeoDataFrame(new_final_dict,crs=3857)


# In[67]:


final_df.to_csv("unicode.csv",index=False)


# In[68]:


len(final_df['name'].unique())


# In[69]:


final_df['name'][0]


# In[70]:


name_1=final_df['name'][0]


# In[71]:


amities['amenity'].unique()


# In[72]:


conventions= {
    'school': 'SCH',
    'place_of_worship': 'TMP',
    'restaurant': 'RES',
    'bus_station': 'BS',
    'cinema': 'CIN',
    'bank': 'BNK',
    'hospital': 'HSP'
}


# In[73]:


name1=final_df['name'][0]


# In[74]:


splited_name=name1.split("--")


# In[75]:


splited_name


# In[76]:


first=splited_name[0]
second=splited_name[1]


# In[77]:


first


# In[78]:


sub_splited=first.split(",")


# In[79]:


sub_splited


# In[80]:


distance=sub_splited[len(sub_splited)-2]
direction=sub_splited[len(sub_splited)-1]


# In[81]:


amenity_name=sub_splited[0]


# In[82]:


name_splited=amenity_name.split(" ")


# In[83]:


name_splited


# In[84]:


convention_name=name_splited[len(name_splited)-1]


# In[85]:


name=name_splited[0]


# In[86]:


name


# In[87]:


name+conventions[convention_name]+distance+direction


# In[88]:


final_df['name'][0]


# In[89]:


def code_generator(name):
    splited_name=name.split("--")
    first=splited_name[0]
    second=splited_name[1]
    first_sub_splited=first.split(",")
    second_sub_splited=second.split(",")
    amenity_first=first_sub_splited[0].split(" ")
    amenity_second=second_sub_splited[0].split(" ")
    amenity_first_name=amenity_first[0]
    amenity_second_name=amenity_second[0]
    amenity_type_first=amenity_first[len(amenity_first)-1]
    amenity_type_second=amenity_second[len(amenity_second)-1]
    distance_first=first_sub_splited[len(first_sub_splited)-2]
    direction_first=second_sub_splited[len(first_sub_splited)-1]
    distance_second=second_sub_splited[len(second_sub_splited)-2]
    direction_second=second_sub_splited[len(second_sub_splited)-1]
    code_first=f"{amenity_first_name}{conventions[amenity_type_first]}{distance_first}{direction_first}"
    code_second=f"{amenity_second_name}{conventions[amenity_type_second]}{distance_second}{direction_second}"
    code=code_first+"-"+code_second
    return code


# In[90]:


for i in list(final_df.index):
    final_df.loc[i,'code']=code_generator(final_df.loc[i,'name'])


# In[91]:


final_df[final_df['code'].duplicated()]


# In[92]:


duplicate_values=[]
for i in list(final_df[final_df['code'].duplicated()]['code']):
    duplicate_values.append(i)
duplicate_values_for_each_names={}
for i in duplicate_values:
    values=list(final_df[final_df['code']==i].index)
    duplicate_values_for_each_names[i]=values
for i in duplicate_values_for_each_names.keys():
    #check length
    for index,value  in enumerate(duplicate_values_for_each_names[i]):
        if index==0:
            pass
        else:
            final_df.loc[value,'code']=final_df.loc[value,'code']+"-"+str(index+1)


# In[ ]:





# In[93]:


final_df.drop(columns=['name'],inplace=True)


# In[94]:


final_df.to_crs('EPSG:4326',inplace=True)


# In[95]:


import folium
tiles=folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                 attr='Esri',
                 name='Esri World Imagery',
                 overlay=True)
map1=final_df[0:1000].explore(tiles=tiles,marker_kwds={'radius':5})
map1.save("buildings.html")


# In[96]:


import folium
tiles=folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                 attr='Esri',
                 name='Esri World Imagery',
                 overlay=True)
map2=amities.explore(tiles=tiles,marker_kwds={'radius':5,'color':'red'})
map2.save("amities.html")


# In[98]:


final_df.t


# In[ ]:




