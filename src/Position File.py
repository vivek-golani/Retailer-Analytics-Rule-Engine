
print('Position File.py started executing')
start = timeit.default_timer()

# =============================================================================
#                       POSITION TAB CALCULATIONS
# =============================================================================

position = all_data[all_data.Month_Order == last][['Zone_Name','New_Area_Code','New_Area_Name','New_Cluster_Name','New_Position_Code','New_Position_Name']].drop_duplicates().sort_values(['Zone_Name','New_Area_Name','New_Cluster_Name','New_Position_Code','New_Position_Name']).dropna()

brands = all_data[['New_Position_Code','Brand']].drop_duplicates().groupby('New_Position_Code', as_index = False).Brand.count()
avg_pob = all_data.groupby('New_Position_Code',as_index = False).Value.sum()
avg_pob['Value'] = round(avg_pob.Value / 6,0)
last_month_pob = round(all_data[all_data.Month_Order == last].groupby('New_Position_Code',as_index = False).Value.sum())
declining_pob = all_data[all_data.Month_Order > last - 3].groupby('New_Position_Code', as_index = False).Value.sum()
declining_pob1 = all_data[all_data.Month_Order > last - 6][all_data.Month_Order < last-2].groupby('New_Position_Code', as_index = False).Value.sum()
declining_pob = pd.merge(declining_pob, declining_pob1, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left').dropna()
declining_pob['L3M/L456M'] = round(declining_pob.Value_x / declining_pob.Value_y,2)
last_month_outlet = all_data[all_data.Month_Order == last][all_data.Categ == 'Chemist'][['New_Position_Code','Retailer_Code']].drop_duplicates().groupby('New_Position_Code', as_index = False).Retailer_Code.count()
outlets = all_data[['New_Position_Code','Retailer_Code']].drop_duplicates().groupby('New_Position_Code', as_index = False).Retailer_Code.count()
chemist_outlets = all_data[all_data.Categ == 'Chemist'][['New_Position_Code','Retailer_Code']].drop_duplicates().groupby('New_Position_Code', as_index = False).Retailer_Code.count()
total_outlets = dvl_shakti.groupby('New_Position_Code', as_index = False).Retailer_Code.count()
avg_brands = all_data[['New_Position_Code','Retailer_Code','Brand']].drop_duplicates().groupby('New_Position_Code', as_index = False).Brand.count()
avg_brands = pd.merge(avg_brands, outlets, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
avg_brands['Avg_Brands'] = round(avg_brands.Brand / avg_brands.Retailer_Code)
avg_vpo = pd.merge(last_month_outlet, last_month_pob, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
avg_vpo['Avg_VPO'] = round(avg_vpo.Value/avg_vpo.Retailer_Code,0)
med_vpo = all_data[all_data.Month_Order == last].groupby(['New_Position_Code','Retailer_Code'], as_index = False).Value.sum()
med_vpo = med_vpo.groupby('New_Position_Code',as_index = False)[['Value']].median().rename(columns = {'Value':'Med_VPO'})
last_pc = all_data[all_data.Month_Order == last][['New_Position_Code','Retailer_Code','Date_Of_Work']].drop_duplicates().groupby('New_Position_Code', as_index = False).count()
vpc = pd.merge(last_month_pob, last_pc[['New_Position_Code','Date_Of_Work']],left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
vpc['Avg_VPC'] = round(vpc.Value / vpc.Date_Of_Work,0)

# =============================================================================
# FINALLY MERGING DIFFERENT DATAFRAMES TO position(CONTAINS DATA FOR ALL POSITIONS)
# =============================================================================

position = pd.merge(position, brands, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, avg_pob, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, last_month_pob, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, declining_pob[['New_Position_Code','L3M/L456M']], on = 'New_Position_Code', how = 'left')
position = pd.merge(position, last_month_outlet, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, chemist_outlets, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, total_outlets, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position['Productivity'] = position.Retailer_Code_x / position.Retailer_Code_y
position = pd.merge(position, avg_brands[['New_Position_Code','Avg_Brands']], left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, avg_vpo[['New_Position_Code','Avg_VPO']], left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, med_vpo, left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, last_pc[['New_Position_Code','Date_Of_Work']], left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = pd.merge(position, vpc[['New_Position_Code','Avg_VPC']], left_on = 'New_Position_Code', right_on = 'New_Position_Code', how = 'left')
position = position.rename(columns = {'Month':'Months_Since_LP', 'L3M/L456M':'Declining_POB', 'Value_x' : 'Avg_Monthly_POB', 'Value_y':'Last_Month_POB', 'Retailer_Code_x' : 'Last_Month_Retailers', 'Retailer_Code_y': 'Chemist_Retailers', 'Retailer_Code':'Total_Retailers', 'Date_Of_Work':'Last_Month_PC'})

# To create a pickle file for later use
#position.to_pickle('Master_Position_Wise.pickle')

# To read position dataframe from pickle file for later purposes
#position = pd.read_pickle('Master_Position_Wise.pickle')
