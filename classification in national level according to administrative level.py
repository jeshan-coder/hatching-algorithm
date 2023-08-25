#!/usr/bin/env python
# coding: utf-8

# In[7]:


import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# In[8]:


wards=gpd.read_file("C:\\hackathon\\base data\\NEPAL_WARDS.shp")


# In[9]:


wards.to_crs('EPSG:4326',inplace=True)


# In[10]:


residence=gpd.read_file("C:\\hackathon\\points\\points.shp")
residence.to_crs('EPSG:4326',inplace=True)


# In[11]:


# residence=gpd.read_file("C:\\hackathon\\pokhara_buildings\\buildings_pkr.shp")
# residence.to_crs('EPSG:4326',inplace=True)


# In[80]:


gravel_road=gpd.read_file("C:\\hackathon\\base data\\\Gravelled_Road.shp")
gravel_road.to_crs('EPSG:4326',inplace=True)


# In[12]:


foot_path=gpd.read_file("C:\\hackathon\\base data\\Foot_Path.shp")
foot_path.to_crs('EPSG:4326',inplace=True)


# In[13]:


highway=gpd.read_file("C:\\hackathon\\base data\\Highway.shp")
highway.to_crs('EPSG:4326',inplace=True)


# In[82]:


gravel_road.drop(columns=['FNODE_','TNODE_','LPOLY_','RPOLY_','LENGTH','ROAD_DD_','ROAD_DD_ID'],inplace=True)


# In[83]:


gravel_road


# In[85]:


foot_path.drop(columns=['FNODE_', 'TNODE_', 'LPOLY_', 'RPOLY_', 'LENGTH', 'ROAD_DD_',
       'ROAD_DD_ID'],inplace=True)


# In[87]:


highway.drop(columns=['FNODE_', 'TNODE_', 'LPOLY_', 'RPOLY_', 'LENGTH', 'ROAD_DD_',
       'ROAD_DD_ID'],inplace=True)


# In[92]:


newdict={}


# In[94]:


type_list=[]
geometry_list=[]
for i in gravel_road['TYPE'].tolist():
    type_list.append(i)
for j in gravel_road['geometry'].tolist():
    geometry_list.append(j)


# In[95]:


for i in foot_path['TYPE'].tolist():
    type_list.append(i)
for j in foot_path['geometry'].tolist():
    geometry_list.append(j)


# In[96]:


for i in highway['TYPE'].tolist():
    type_list.append(i)
for j in highway['geometry'].tolist():
    geometry_list.append(j)


# In[97]:


newdict['TYPE']=type_list
newdict['geometry']=geometry_list


# In[102]:


road_network=gpd.GeoDataFrame(newdict,crs='EPSG:4326')


# In[ ]:





# In[14]:


river=gpd.read_file("C:\\hackathon\\base data\\River.shp")
river.to_crs('EPSG:4326',inplace=True)


# In[15]:


gravel=gpd.read_file("C:\\hackathon\\base data\\Gravelled_Road.shp")
gravel.to_crs('EPSG:4326',inplace=True)


# In[16]:


fig,ax=plt.subplots(figsize=(16,9))
wards.plot(ax=ax)
residence.plot(color='red',ax=ax)
foot_path.plot(color='green',ax=ax)
highway.plot(color='black',ax=ax)
river.plot(color='pink',ax=ax)
gravel.plot(color='yellow',ax=ax)


# In[17]:


residence


# In[18]:


wards.drop(columns=['OBJECTID'],inplace=True)


# In[19]:


len(wards['DCODE'].unique())


# In[20]:


wards['DAS'].unique()


# In[21]:


wards.columns


# In[22]:


wards['GN_CODE'].unique()


# In[23]:


wards['Type_GN'].unique()


# In[24]:


wards.drop(columns=['DAN','DAS','GN_CODE','DDGNWW','CENTER','DDGN'],inplace=True)


# In[25]:


wards.drop(columns=['Area_SQKM','Shape_Leng','Shape_Area'],inplace=True)


# In[26]:


wards


# In[27]:


first_point=residence['geometry'][0]


# In[28]:


#finding points lies in which state,district,ward number and nagarpalika
new_list=[]
for index,value in enumerate(wards['geometry']):
    for j,i in enumerate(residence['geometry']):
        point=i
        if value.contains(point)==True:
            newdict={}
            newdict['DCODE']=wards.loc[index,'DCODE']
            newdict['DCODE']=wards.loc[index,'DCODE']
            newdict['DISTRICT']=wards.loc[index,'DISTRICT']
            newdict['GaPa_NaPa']=wards.loc[index,'GaPa_NaPa']
            newdict['Type_GN']=wards.loc[index,'Type_GN']
            newdict['WARD_NO']=wards.loc[index,'NEW_WARD_N']
            newdict['STATE_CODE']=wards.loc[index,'STATE_CODE']
            newdict['geometry']=i
            new_list.append(newdict)


# In[29]:


points_with_info=gpd.GeoDataFrame(new_list,crs='EPSG:4326')


# In[30]:


points_with_info


# In[31]:


d_codes={}
for i,j in zip(wards['DCODE'],wards['DISTRICT']):
    if j in d_codes.keys():
        pass
    else:
        d_codes[j]=i


# In[32]:


district_codes=pd.DataFrame({'DISTRICTS':list(d_codes.keys()),'DCODE':list(d_codes.values())})


# In[33]:


district_codes


# In[34]:


district_codes.to_csv("C:\\hackathon\\district codes\\district_codes.csv",index=False)


# In[35]:


for i in wards['DISTRICT'].unique():
    wards_map={}
    wards_data=wards[wards['DISTRICT']==i]['GaPa_NaPa'].unique().tolist()
    for index,value in enumerate(wards_data):
        wards_map[value]=index+1
    gp_np_df=pd.DataFrame({'GaPa_NaPa':list(wards_map.keys()),'G_CODE':list(wards_map.values())})
    gp_np_df.to_csv(f"C:\hackathon\gapa_napa mapping\\{i}.csv",index=False)


# In[36]:


gp_np_df


# ## Generating new registration Number

# In[37]:


points_with_info_copy=points_with_info.copy()


# In[38]:


district_codes=pd.read_csv("C:\\hackathon\\district codes\\district_codes.csv")


# In[39]:


points_with_info


# In[40]:


points_with_info


# In[41]:


#assigning unique code to gaupalika or nagar palika
for index in points_with_info.index:
    district=points_with_info.loc[index,'DISTRICT']
    gapa_name=points_with_info.loc[index,'GaPa_NaPa']
    GPNP_df=pd.read_csv(f"C:\\hackathon\\gapa_napa mapping\\{district}.csv")
    GPNP_CODE=GPNP_df[GPNP_df['GaPa_NaPa']==gapa_name]['G_CODE'].tolist()[0]
    points_with_info.loc[index,'GPNP_CODE']=GPNP_CODE
points_with_info['GPNP_CODE']=points_with_info['GPNP_CODE'].astype('int64')


# In[42]:


nn=points_with_info


# In[43]:


#registration number


# In[44]:


points_with_info


# In[45]:


type(nn['GPNP_CODE'][0])


# In[46]:


nn


# In[47]:


reg=f"{STATE_CODE}-{DCODE}-{GPNP_CODE}-{WARD_NO}"


# In[48]:


for i in nn.index:
    STATE_CODE=nn['STATE_CODE'][i]
    DCODE=nn['DCODE'][i]
    GPNP_CODE=nn['GPNP_CODE'][i]
    WARD_NO=nn['WARD_NO'][i]
    reg=f"{STATE_CODE}-{DCODE}-{GPNP_CODE}-{WARD_NO}"
    nn.loc[i,'reg']=reg


# In[49]:


nn


# In[50]:


nn[nn['reg']=='1-4-15.0-8'].index.tolist()


# In[51]:


for i in list(nn['reg'].unique()):
    indexes=nn[nn['reg']==i].index.tolist()
    for index,value in enumerate(indexes):
        nn.loc[value,'HOUSE_NO']=index+1
nn['HOUSE_NO']=nn['HOUSE_NO'].astype('int64')


# In[52]:


nn


# In[53]:


nn


# In[54]:


for i in nn.index:
    nn.loc[i,'HOUSE_REG']=nn.loc[i,'reg']+"-"+str(nn.loc[i,'HOUSE_NO'])


# In[55]:


nn.drop(columns=['DCODE','WARD_NO','GPNP_CODE','reg'],inplace=True)


# In[56]:


int(nn['HOUSE_NO'][0])


# In[57]:


nn


# In[ ]:





# In[ ]:





# In[ ]:





# In[105]:


road_network


# In[58]:


import folium


# In[103]:


tiles=folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                 attr='Esri',
                 name='Esri World Imagery',
                 overlay=True)
road_network.explore(tiles=tiles,marker_kwds={'radius':20})


# In[104]:


residence


# ### 
