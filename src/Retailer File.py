
print('Retailer File.py started executing')
start = timeit.default_timer()

# =============================================================================
#                       RETAILER TAB CALCULATIONS
# =============================================================================

last = all_data.Month_Order.max()
last_pob = all_pob.Month_Order.max()

retailer = all_data[['Retailer_Code','Zone_Name','New_Area_Code','New_Area_Name','New_Cluster_Name','New_Position_Code','New_Position_Name','New_Beat_Code','New_Beat_Name']].drop_duplicates().sort_values(['Zone_Name','New_Area_Name','New_Cluster_Name','New_Position_Code','New_Position_Name','New_Beat_Code','New_Beat_Name','Retailer_Code']).dropna()

retailer_name = all_data.groupby('Retailer_Code', as_index = False).Month_Order.max()
retailer_name = pd.merge(retailer_name, all_data[['Retailer_Code','Month_Order','Retailer_Name','Categ','Beat_Code']].drop_duplicates(), on = ['Retailer_Code','Month_Order'], how = 'left').sort_values('Month_Order',ascending = False)
retailer_name = retailer_name.groupby('Retailer_Code',as_index = False).first()
retailer = pd.merge(retailer,retailer_name[['Retailer_Code','Retailer_Name','Categ']], on = 'Retailer_Code', how = 'left')
brands = all_data[['Retailer_Code','Brand']].drop_duplicates().groupby('Retailer_Code', as_index = False).Brand.count()
last_month_pob = round(all_data[all_data.Month_Order == last].groupby('Retailer_Code',as_index = False).Value.sum())
declining_pob = all_data[['Retailer_Code']].drop_duplicates()
declining_pob1 = all_data[all_data.Month_Order > last - 3].groupby('Retailer_Code', as_index = False).agg({'Value': 'sum', 'Month' : 'nunique'})
declining_pob1['L3M'] = declining_pob1.Value #/ declining_pob.Month
declining_pob2 = all_data[all_data.Month_Order > last - 6][all_data.Month_Order < last-2].groupby('Retailer_Code', as_index = False).agg({'Value': 'sum', 'Month' : 'nunique'})
declining_pob2['L456M'] = declining_pob2.Value #/ declining_pob1.Month
declining_pob = pd.merge(declining_pob, declining_pob1[['Retailer_Code','L3M']], on = 'Retailer_Code', how = 'left')
declining_pob = pd.merge(declining_pob, declining_pob2[['Retailer_Code','L456M']], on = 'Retailer_Code', how = 'left')
months_since_lp = all_data.groupby('Retailer_Code',as_index = False).Month_Order.max()
months_since_lp['Month_Order'] = last - months_since_lp['Month_Order'] + 1

all_pob = all_pob[all_pob.Value > 0]

active_months = all_pob.groupby('Retailer_Code',as_index = False).agg({'Month_Order':['min', 'nunique']})
active_months = pd.merge(retailer[['Retailer_Code']], active_months, left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left')
active_months = active_months.rename(columns = {('Month_Order','min') : 'Mo_min' , ('Month_Order', 'nunique') : 'Mo_unique_12'})
active_months['Tenure'] = np.where(active_months['Mo_min'] < 6, 6, last_pob - active_months['Mo_min'] + 1)

declining_pob = pd.merge(declining_pob, active_months[['Retailer_Code','Tenure']], on = 'Retailer_Code', how = 'left')
temp = declining_pob.dropna()
temp['L3M/L456M'] = round(temp.L3M / temp.L456M,2)
temp['L3M/L456M'] = np.where(np.isinf(temp['L3M/L456M']), 0, temp['L3M/L456M'])

t = declining_pob[~declining_pob.Retailer_Code.isin(temp.Retailer_Code)]
t['L3M/L456M'] = ''
t['L3M/L456M'] = np.where(np.isnan(t['L3M']), 0 , t['L3M/L456M'])
t['L3M/L456M'] = np.where(np.isnan(t['L456M']), np.where(t['Tenure'] < 4,1000, 0), t['L3M/L456M'])
declining_pob = temp.append(t, ignore_index = True)

avg_pob = all_data.groupby('Retailer_Code',as_index = False).Value.sum()
avg_pob = pd.merge(avg_pob, active_months[['Retailer_Code','Tenure']], on = 'Retailer_Code', how = 'left')
avg_pob['Value'] = round(avg_pob.Value / avg_pob.Tenure)

a = all_pob[all_pob.Month_Order > last_pob - 6].groupby('Retailer_Code',as_index = False).agg({'Month_Order':'nunique'}).dropna()
active_months = pd.merge(active_months, a, left_on = 'Retailer_Code', right_on = 'Retailer_Code',how = 'left')
active_months['Active_Months'] = active_months.Month_Order / active_months.Tenure

last_pc = all_data[all_data.Month_Order == last][['Retailer_Code','Date_Of_Work']].drop_duplicates().groupby('Retailer_Code', as_index = False).count()
vpc = pd.merge(last_month_pob, last_pc[['Retailer_Code','Date_Of_Work']],left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left')
vpc['Avg_VPC'] = round(vpc.Value / vpc.Date_Of_Work)

# =============================================================================
# FINALLY MERGING DIFFERENT DATAFRAMES TO retailer(CONTAINS DATA FOR ALL RETAILERS)
# =============================================================================

retailer = pd.merge(retailer, brands, left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left')
retailer = pd.merge(retailer, avg_pob[['Retailer_Code','Value']], left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left')
retailer = pd.merge(retailer, last_month_pob, left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left').fillna(0)
retailer = pd.merge(retailer, declining_pob[['Retailer_Code','L3M/L456M']], left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left')
retailer = pd.merge(retailer, months_since_lp, left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left')
retailer = pd.merge(retailer, active_months[['Retailer_Code','Tenure','Active_Months']], left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left')
retailer = pd.merge(retailer, last_pc, left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left').fillna(0)
retailer = pd.merge(retailer, vpc[['Retailer_Code','Avg_VPC']], left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left').fillna(0)
retailer = retailer.rename(columns = {'Month_Order':'Months_Since_LP','Value_x' : 'Avg_Monthly_POB','Value_y':'Last_Month_POB','Date_Of_Work' : 'Last_Month_PC', 'L3M/L456M': 'Declining_POB'})
clus = retailer.groupby('New_Cluster_Name', as_index = False).Brand.max()
retailer = pd.merge(retailer, clus, left_on = 'New_Cluster_Name', right_on = 'New_Cluster_Name', how = 'left')
retailer = retailer.rename(columns = {'Brand_x': 'Brand', 'Brand_y' : 'Max_Brand_Cluster'})
retailer['Brands_Percent'] = retailer.Brand/retailer.Max_Brand_Cluster
retailer['Position'] = retailer['New_Position_Code'].astype(str) + '-' + retailer['New_Position_Name']

recent = retailer[retailer.Categ == 'Chemist'][retailer['Declining_POB'] == 1000]

retailer['Declining_POB'] = np.where(retailer['Declining_POB'] == 1000, 0,np.where(retailer['Declining_POB'] == -1, 0, retailer['Declining_POB']))

# To create a pickle file for later use
#retailer.to_pickle('Master_Retailer_Wise.pickle')

# To read retailer dataframe from pickle file for later purposes
#retailer = pd.read_pickle('Master_Retailer_Wise.pickle')

# =============================================================================
# REMOVING UNWANTED DATAFRAMES TO REDUCE RAM USAGE
# =============================================================================

del a, active_months, avg_brands, avg_pob, avg_sec, brands, declining_pob, declining_pob1, declining_pob2
del last_month_pob, last_pc, months_since_lp, t, temp, vpc, 