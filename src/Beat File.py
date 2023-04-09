
print('Beat File.py started executing')
start = timeit.default_timer()

# =============================================================================
#                       BEAT TAB CALCULATIONS
# =============================================================================

beat = all_data[all_data.Month_Order == last][['Zone_Name','New_Area_Code','New_Area_Name','New_Cluster_Name','New_Position_Code','New_Position_Name','New_Beat_Code','New_Beat_Name']].drop_duplicates().sort_values(['Zone_Name','New_Area_Name','New_Cluster_Name','New_Position_Code','New_Position_Name','New_Beat_Code','New_Beat_Name']).dropna()

brands = all_data[['New_Beat_Code','Brand']].drop_duplicates().groupby('New_Beat_Code', as_index = False).Brand.count()
avg_pob = all_data.groupby('New_Beat_Code',as_index = False).Value.sum()
avg_pob['Value'] = round(avg_pob.Value / 6,0)
last_month_pob = round(all_data[all_data.Month_Order == last].groupby('New_Beat_Code',as_index = False).Value.sum())
declining_pob = all_data[all_data.Month_Order > last - 3].groupby('New_Beat_Code', as_index = False).Value.sum()
declining_pob1 = all_data[all_data.Month_Order > last - 6][all_data.Month_Order < last-2].groupby('New_Beat_Code', as_index = False).Value.sum()
declining_pob = pd.merge(declining_pob, declining_pob1, left_on = 'New_Beat_Code', right_on = 'New_Beat_Code', how = 'left').dropna()
declining_pob['L3M/L456M'] = round(declining_pob.Value_x / declining_pob.Value_y,2)
last_month_outlet = all_data[all_data.Month_Order == last][all_data.Categ == 'Chemist'][['New_Beat_Code','Retailer_Code']].drop_duplicates().groupby('New_Beat_Code', as_index = False).Retailer_Code.count()
outlets = all_data[['New_Beat_Code','Retailer_Code']].drop_duplicates().groupby('New_Beat_Code', as_index = False).Retailer_Code.count()
chemist_outlets = all_data[all_data.Categ == 'Chemist'][['New_Beat_Code','Retailer_Code']].drop_duplicates().groupby('New_Beat_Code', as_index = False).Retailer_Code.count()
total_outlets = dvl_shakti.groupby('New_Beat_Code', as_index = False).Retailer_Code.count()
avg_brands = all_data[['New_Beat_Code','Retailer_Code','Brand']].drop_duplicates().groupby('New_Beat_Code', as_index = False).Brand.count()
avg_brands = pd.merge(avg_brands, outlets, left_on = 'New_Beat_Code', right_on = 'New_Beat_Code', how = 'left')
avg_brands['Avg_Brands'] = round(avg_brands.Brand / avg_brands.Retailer_Code)
avg_vpo = pd.merge(last_month_outlet, last_month_pob, left_on = 'New_Beat_Code', right_on = 'New_Beat_Code', how = 'left')
avg_vpo['Avg_VPO'] = round(avg_vpo.Value/avg_vpo.Retailer_Code,0)
med_vpo = all_data[all_data.Month_Order == last].groupby(['New_Beat_Code','Retailer_Code'], as_index = False).Value.sum()
med_vpo = med_vpo.groupby('New_Beat_Code',as_index = False)[['Value']].median().rename(columns = {'Value':'Med_VPO'})
last_pc = all_data[all_data.Month_Order == last][['New_Beat_Code','Retailer_Code','Date_Of_Work']].drop_duplicates().groupby('New_Beat_Code', as_index = False).count()
vpc = pd.merge(last_month_pob, last_pc[['New_Beat_Code','Date_Of_Work']],left_on = 'New_Beat_Code', right_on = 'New_Beat_Code', how = 'left')
vpc['Avg_VPC'] = round(vpc.Value / vpc.Date_Of_Work,0)

# =============================================================================
# FINALLY MERGING DIFFERENT DATAFRAMES TO beat(CONTAINS DATA FOR ALL BEATS)
# =============================================================================

beat = pd.merge(beat, brands, on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, avg_pob, on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, last_month_pob, on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, declining_pob[['New_Beat_Code','L3M/L456M']], on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, last_month_outlet, on = 'New_Beat_Code',  how = 'left')
beat = pd.merge(beat, chemist_outlets, on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, total_outlets, on = 'New_Beat_Code', how = 'left')
beat['Productivity'] = beat.Retailer_Code_x / beat.Retailer_Code_y
beat = pd.merge(beat, avg_brands[['New_Beat_Code','Avg_Brands']], on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, avg_vpo[['New_Beat_Code','Avg_VPO']], on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, med_vpo, on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, last_pc[['New_Beat_Code','Date_Of_Work']], on = 'New_Beat_Code', how = 'left')
beat = pd.merge(beat, vpc[['New_Beat_Code','Avg_VPC']], on = 'New_Beat_Code', how = 'left')
beat = beat.rename(columns = {'Month':'Months_Since_LP', 'L3M/L456M':'Declining_POB', 'Value_x' : 'Avg_Monthly_POB', 'Value_y':'Last_Month_POB', 'Retailer_Code_x' : 'Last_Month_Retailers', 'Retailer_Code_y': 'Chemist_Retailers', 'Retailer_Code':'Total_Retailers', 'Date_Of_Work':'Last_Month_PC'})
beat['Position'] = beat['New_Position_Code'].astype(str) + '-' + beat['New_Position_Name']

# To create a pickle file for later use
#beat.to_pickle('Master_Beat_Wise.pickle')

# To read beat dataframe from pickle file for later purposes
#beat = pd.read_pickle('Master_Beat_Wise.pickle')
