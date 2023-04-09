
print('Update.py started executing')
start = timeit.default_timer()

# =============================================================================
# ADDING A COLUMNS Categ FOR DIVIDING INTO CHEMIST & NON-CHEMIST
# =============================================================================

all_data['Category'] = all_data['Category'].str.title()
all_data['Categ'] = np.where(all_data['Category'] == 'Medical','Chemist','Non-Chemist')

# =============================================================================
# UPDATING all_data AND dvl_shakti FOR LATEST AREA, CLUSTER & POSITION
# =============================================================================

update = all_data.groupby('Retailer_Code',as_index = False).Month_Order.max()
update = pd.merge(update,all_data[['Retailer_Code', 'Month_Order','Beat_Code']].drop_duplicates(), on = ['Retailer_Code','Month_Order'],  how = 'left').sort_values('Month_Order',ascending = False)
update = update.groupby('Retailer_Code', as_index = False).first()

'''update_position = all_data.groupby('Beat_Code', as_index = False).Month_Order.max()
update_position = pd.merge(update_position,all_data[['Beat_Code', 'Month_Order','Position_Code','Position_Name']].drop_duplicates(), on = ['Beat_Code','Month_Order'],  how = 'left').sort_values('Month_Order',ascending = False)
update_position = update_position.groupby('Beat_Code', as_index = False).first()

update_cluster = all_data.groupby('Position_Code',as_index = False).Month_Order.max()
update_cluster = pd.merge(update_cluster, all_data[['Position_Code','Month_Order','Cluster_Code','Cluster_Name','Area_Code','Area_Name']].drop_duplicates(), on = ['Position_Code','Month_Order'], how ='left')
update_cluster = update_cluster.groupby('Position_Code', as_index = False).first()'''


update = pd.merge(update,dvl_shakti[['Beat_Code','Beat_Name','Position_Code','Position_Name','Cluster_Code','Cluster_Name','Area_Code','Area_Name']].drop_duplicates(), on = 'Beat_Code', how ='left')
update = update.rename(columns = {'Area_Code' : 'New_Area_Code', 'Area_Name' : 'New_Area_Name', 'Cluster_Code' : 'New_Cluster_Code', 'Cluster_Name' : 'New_Cluster_Name', 'Position_Code' : 'New_Position_Code', 'Position_Name' : 'New_Position_Name', 'Beat_Code' : 'New_Beat_Code', 'Beat_Name' : 'New_Beat_Name'})
update = update.drop(columns = ['Month_Order'])

#Updating relevant dataframes with new Cluster and Position
all_data = pd.merge(all_data, update, on = 'Retailer_Code', how ='left')
dvl_shakti = dvl_shakti.rename(columns = {'Area_Code' : 'New_Area_Code', 'Area_Name' : 'New_Area_Name', 'Cluster_Code' : 'New_Cluster_Code', 'Cluster_Name' : 'New_Cluster_Name', 'Position_Code' : 'New_Position_Code', 'Position_Name' : 'New_Position_Name', 'Beat_Code' : 'New_Beat_Code', 'Beat_Name' : 'New_Beat_Name'})
# =============================================================================
#                   QC Statements- Uncomment to check
# =============================================================================

# all_data.New_Cluster_Code.unique()
# all_data.New_Position_Code.unique()

'''position = all_data[['Zone_Name','New_Area_Code','New_Cluster_Code','New_Position_Code']].drop_duplicates().sort_values(['Zone_Name','Area_Name','New_Cluster_Name','New_Position_Code']).dropna()
temp = position.groupby('New_Position_Code',as_index = False).count()
temp = temp[temp.New_Cluster_Name > 1]
if len(temp):
    print('1 position in 2 clusters')'''


# =============================================================================
# last HAS THE VALUE 6 AS TOTAL NO. OF MONTHS IS 6 AND HENCE MAX Month_Order = 6
# =============================================================================

last = all_data.Month_Order.max()

# =============================================================================
# REMOVING UNWANTED DATAFRAMES TO REDUCE RAM USAGE
# =============================================================================

del update
