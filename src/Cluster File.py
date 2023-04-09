
print('Cluster File.py started executing')
start = timeit.default_timer()

# =============================================================================
#                       CLUSTER TAB CALCULATIONS
# =============================================================================

cluster = all_data[all_data.Month_Order == last][['Zone_Name','New_Area_Code','New_Area_Name','New_Cluster_Code','New_Cluster_Name']].drop_duplicates().sort_values(['Zone_Name','New_Area_Name','New_Cluster_Code','New_Cluster_Name']).dropna()

avg_pob = all_data.groupby('New_Cluster_Code',as_index = False).Value.sum()
avg_pob['Value'] = round(avg_pob.Value / 6,0)
avg_sec = sec.groupby('Cluster_Code', as_index = False).Value.sum()
avg_sec = avg_sec[avg_sec.Value > 0]
avg_sec['Value'] = round(avg_sec.Value / 6,0)
last_month_pob = round(all_data[all_data.Month_Order == last].groupby('New_Cluster_Code',as_index = False).Value.sum())
last_month_sec = sec[sec.Month_Order == last].groupby('Cluster_Code',as_index = False).Value.sum()
last_month_sec = round(last_month_sec[last_month_sec.Value != 0])
declining_sec = sec[sec.Month_Order > last - 3].groupby('Cluster_Code', as_index = False).Value.sum()
declining_sec = declining_sec[declining_sec.Value > 0]
declining_sec1 = sec[sec.Month_Order > last - 6][sec.Month_Order < last-2].groupby('Cluster_Code', as_index = False).Value.sum()
declining_sec1 = declining_sec1[declining_sec1.Value > 0]
declining_sec = pd.merge(declining_sec, declining_sec1, left_on = 'Cluster_Code', right_on = 'Cluster_Code', how = 'left')
declining_sec['L3M/L456M'] = round(declining_sec.Value_x / declining_sec.Value_y,2)
last_month_outlet = all_data[all_data.Month_Order == last][all_data.Categ == 'Chemist'][['New_Cluster_Code','Retailer_Code']].drop_duplicates().groupby('New_Cluster_Code', as_index = False).Retailer_Code.count()
outlets = all_data[['New_Cluster_Code','Retailer_Code']].drop_duplicates().groupby('New_Cluster_Code', as_index = False).Retailer_Code.count()
chemist_outlets = all_data[all_data.Categ == 'Chemist'][['New_Cluster_Code','Retailer_Code']].drop_duplicates().groupby('New_Cluster_Code', as_index = False).Retailer_Code.count()
total_outlets = dvl_shakti.groupby('New_Cluster_Code', as_index = False).Retailer_Code.count()
avg_brands = all_data[['New_Cluster_Code','Retailer_Code','Brand']].drop_duplicates().groupby('New_Cluster_Code', as_index = False).Brand.count()
avg_brands = pd.merge(avg_brands, outlets, left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
avg_brands['Avg_Brands'] = round(avg_brands.Brand / avg_brands.Retailer_Code,0)
avg_vpo = pd.merge(last_month_outlet, last_month_pob, left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
avg_vpo['Avg_VPO'] = round(avg_vpo.Value/avg_vpo.Retailer_Code,0)
med_vpo = all_data[all_data.Month_Order == last].groupby(['New_Cluster_Code','Retailer_Code'], as_index = False).Value.sum()
med_vpo = med_vpo.groupby('New_Cluster_Code',as_index = False)[['Value']].median().rename(columns = {'Value':'Med_VPO'})
last_pc = all_data[all_data.Month_Order == last][['New_Cluster_Code','Retailer_Code','Date_Of_Work']].drop_duplicates().groupby('New_Cluster_Code', as_index = False).count()
vpc = pd.merge(last_month_pob, last_pc[['New_Cluster_Code','Date_Of_Work']],left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
vpc['Avg_VPC'] = round(vpc.Value / vpc.Date_Of_Work,0)
pob_sec = pd.merge(avg_pob[['New_Cluster_Code','Value']], avg_sec, left_on = 'New_Cluster_Code', right_on = 'Cluster_Code', how = 'left')
pob_sec['Pob_Sec'] = (pob_sec.Value_x - pob_sec.Value_y)/pob_sec.Value_x

# =============================================================================
# FINALLY MERGING DIFFERENT DATAFRAMES TO cluster(CONTAINS DATA FOR ALL CLUSTERS)
# =============================================================================

cluster = pd.merge(cluster, avg_pob, left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, last_month_pob, left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, last_month_sec, left_on = 'New_Cluster_Code', right_on = 'Cluster_Code', how = 'left').drop(columns = ['Cluster_Code'])
cluster = pd.merge(cluster, declining_sec[['Cluster_Code','L3M/L456M']], left_on = 'New_Cluster_Code', right_on = 'Cluster_Code', how = 'left').drop(columns = ['Cluster_Code'])
cluster = pd.merge(cluster, total_outlets, left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, chemist_outlets, left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, last_month_outlet, left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster['Productivity'] = cluster.Retailer_Code / cluster.Retailer_Code_y
cluster = pd.merge(cluster, avg_brands[['New_Cluster_Code','Avg_Brands']], left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, avg_vpo[['New_Cluster_Code','Avg_VPO']], left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, med_vpo, left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, last_pc[['New_Cluster_Code','Date_Of_Work']], left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, vpc[['New_Cluster_Code','Avg_VPC']], left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = pd.merge(cluster, pob_sec[['New_Cluster_Code','Pob_Sec']], left_on = 'New_Cluster_Code', right_on = 'New_Cluster_Code', how = 'left')
cluster = cluster.rename(columns = {'Value_x' : 'Avg_Monthly_POB', 'Value_y' : 'Last_Month_POB', 'Value' : 'Last_Month_Sec', 'L3M/L456M':'Declining_Sec','Retailer_Code_x' : 'Total_Retailers','Retailer_Code_y': 'Chemist_Retailers','Retailer_Code':'Last_Month_Retailers','Date_Of_Work' : 'Last_Month_PC'})

# To create a pickle for later use
#cluster.to_pickle(path + '\Pickle Files\Master_Cluster_Wise.pickle')

# To read cluster dataframe from pickle file for later purposes
#cluster = pd.read_pickle('Master_Cluster_Wise.pickle')