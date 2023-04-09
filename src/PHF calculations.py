
data1 = pd.read_pickle(path + '/Pickle Files/pob_h1_2019.pickle')
data2 = pd.read_pickle(path + '/Pickle Files/pob_h2_2019.pickle')
data3 = pd.read_pickle(path + '/Pickle Files/pob_h1_2020.pickle')

data1['Category'] = data1['Category'].str.title()
data2['Category'] = data2['Category'].str.title()
data2['Category'] = np.where(data2['Category'] == 'Cosmetic','Cosmetics',data2['Category'])
data3['Category'] = data3['Category'].str.title()

all_data = data1.append(data2, ignore_index = True)
all_data = all_data.append(data3, ignore_index = True)

del data1, data2, data3


###########################    Adding Month    #############################
###########################       Order        #############################

temp = all_data[['Month','Year']].drop_duplicates().reset_index().drop(columns = ['index'])
arr = np.array([])
for i in range(1,10):
    arr = np.append(arr,i)
temp['Month_Order'] = pd.DataFrame(arr)
temp['Month_Order'] = temp.Month_Order.astype(int)

all_data = pd.merge(all_data,temp, on = ['Month','Year'], how = 'left')


branch = pd.read_excel(path + '/Retailer Segmentation/RARE Branches.xlsx')
branch = branch[~pd.isna(branch.Branch)]

branch = pd.merge(branch, all_data[['Retailer_Code','Category']].drop_duplicates(), on = 'Retailer_Code' , how = 'left').sort_values('Category', ascending = False)
branch = branch.groupby('Retailer_Code', as_index = False).first()

###########################    Category of    #############################
###########################     Retailers     #############################

#all_data.groupby('Category',as_index = False).size()
branch.groupby('Category',as_index = False).size()

###########################    Margin of    #############################
###########################    Retailers    #############################

sku_list = [400134002,400127018,401285006]
filter_data = all_data[all_data.Sku_Code.isin(sku_list)]

retailer = all_data[['Retailer_Code','Retailer_Name']].drop_duplicates()
retailer = retailer.groupby('Retailer_Code',as_index = False).first()


vals = filter_data.groupby(['Retailer_Code','Sku_Code','Sku_Name'], as_index = False).agg({'Value': 'sum', 'Order_Qty':'sum'})
vals = pd.merge(vals, retailer, on = 'Retailer_Code', how = 'left')
vals['Unit Cost'] = vals.Value / vals.Order_Qty
ret = vals[['Retailer_Code','Retailer_Name','Sku_Name','Unit Cost']]
ret = pd.pivot_table(ret, values = ['Unit Cost'], index = ['Retailer_Code','Retailer_Name'], columns = ['Sku_Name']).reset_index()
ret.columns = ["_".join((j,i)) for i,j in ret.columns]
ret = ret.rename(columns = {'_Retailer_Code':'Retailer_Code' , '_Retailer_Name':'Retailer_Name', 'Digeplex 200 ml_Unit Cost' : 'Digeplex', 'Saridon 20s Monocarton_Unit Cost' : 'Saridon', 'Supradyn Tablets 15S_Unit Cost' : 'Supradyn'})

t = pd.DataFrame(ret.Supradyn.unique())

t = pd.DataFrame(ret.Saridon.unique())

t = pd.DataFrame(ret.Digeplex.unique())

del filter_data
 
########################### Low Stock & High Stock  #############################
###########################       Retailers         #############################
 
pob = all_data.groupby('Retailer_Code',as_index = False).Value.sum()
active_months = all_data.groupby('Retailer_Code',as_index = False).agg({'Month_Order':['min','nunique']})
last = all_data.Month_Order.max()

pob = pd.merge(pob, active_months, on = 'Retailer_Code' , how = 'left')
pob = pob.rename(columns = {('Month_Order','min') : 'Mo_min' , ('Month_Order', 'nunique') : 'Mo_unique_12'})
pob['Tenure'] = last - pob['Mo_min'] + 1
pob['Valpermonth_Shakti'] = pob.Value / pob.Tenure

branch = pd.merge(branch,pob, on = 'Retailer_Code', how = 'left')
val_median = branch.Value.median()
mo_median = branch.Mo_unique_12.median()
branch['Rotation'] = ''
branch['Rotation'] = np.where(branch['Value'] > val_median, np.where(branch['Mo_unique_12'] >= 7, 'High', 'Low'),'Low')
branch['Rotation'] = np.where(branch['Rotation'] == '','Low',branch['Rotation'])

branch.groupby('Rotation', as_index = False).size()

########################### Quarter wise values #############################
###########################                     #############################

q1 = all_data[all_data.Month_Order < 4]
pob1 = q1.groupby('Retailer_Code',as_index = False).Value.sum()
pob1 = pob1.rename(columns = { 'Value' : 'Q1' })

q2 = all_data[all_data.Month_Order > 3][all_data.Month_Order < 7]
pob2 = q2.groupby('Retailer_Code',as_index = False).Value.sum()
pob2 = pob2.rename(columns = { 'Value' : 'Q2' })

q3 = all_data[all_data.Month_Order > 6]
pob3 = q3.groupby('Retailer_Code',as_index = False).Value.sum()
pob3 = pob3.rename(columns = { 'Value' : 'Q3' })


branch = pd.merge(branch, pob1, on = ['Retailer_Code'], how = 'left')
branch = pd.merge(branch, pob2, on = ['Retailer_Code'], how = 'left')
branch = pd.merge(branch, pob3, on = ['Retailer_Code'], how = 'left')


########################### Significant Increase in #############################
###########################        Turnover         #############################

retailer = all_data[['Retailer_Code','Retailer_Name']].drop_duplicates()
retailer = retailer.groupby('Retailer_Code',as_index = False).first()

declining_pob1 = all_data[all_data.Month_Order > last - 3].groupby('Retailer_Code', as_index = False).agg({'Value': 'sum', 'Month' : 'nunique'})
declining_pob1['L3M'] = declining_pob1.Value #/ declining_pob.Month
declining_pob2 = all_data[all_data.Month_Order > last - 6][all_data.Month_Order < last-2].groupby('Retailer_Code', as_index = False).agg({'Value': 'sum', 'Month' : 'nunique'})
declining_pob2['L456M'] = declining_pob2.Value #/ declining_pob1.Month
declining_pob3 = all_data[all_data.Month_Order < last-5].groupby('Retailer_Code', as_index = False).agg({'Value': 'sum', 'Month' : 'nunique'})
declining_pob3['L789M'] = declining_pob3.Value #/ declining_pob1.Month

retailer = pd.merge(retailer, declining_pob1[['Retailer_Code', 'L3M']], on = 'Retailer_Code', how = 'left').fillna(0)
retailer = pd.merge(retailer, declining_pob2[['Retailer_Code', 'L456M']], on = 'Retailer_Code', how = 'left').fillna(0)
retailer = pd.merge(retailer, declining_pob3[['Retailer_Code', 'L789M']], on = 'Retailer_Code', how = 'left').fillna(0)
retailer['L3M/L456M'] = (retailer.L3M - retailer.L456M) / retailer.L456M
retailer['L456M/L789M'] = (retailer.L456M - retailer.L789M) / retailer.L789M
retailer = retailer.fillna(0)

retailer['Trend'] = (retailer['L3M/L456M'] + retailer['L456M/L789M'])/2
retailer['Trend'] = np.where(np.isinf(retailer['Trend']), np.where(~np.isinf(retailer['L3M/L456M']),retailer['L3M/L456M'],retailer['Trend']), retailer['Trend'])
retailer['Trend'] = np.where(np.isinf(retailer['Trend']), np.where(~np.isinf(retailer['L456M/L789M']),retailer['L456M/L789M'],10),retailer['Trend'])
retailer['Trend'] = np.where(np.isinf(retailer['Trend']), 10, retailer['Trend'])
branch = pd.merge(branch, retailer[['Retailer_Code','Trend']], on = 'Retailer_Code', how = 'left')

del declining_pob1,declining_pob2,declining_pob3
###########################  Operating in Lockdown   #############################
###########################                         #############################

lockdown = pd.read_excel(path + '/ShaktiAprMay.xlsx')
lockdown.columns = lockdown.columns.str.replace(' ','_')
lockdown.columns = lockdown.columns.str.title()
lockdown = lockdown.rename(columns = {'Sum([Ordered_Qty])' : 'Order_Qty', 'Sum([Pob_Value])' : 'Value'})
temp = lockdown.groupby('Retailer_Code', as_index = False).Value.sum()

branch = pd.merge(branch, temp, on = 'Retailer_Code', how = 'left').fillna(0)
branch = branch.rename(columns = {'Value_y' : 'Lockdown Value'})
branch['Lockdown Active'] = np.where(branch['Lockdown Value'] > 0, 'Yes', 'No')

###########################    Trishul Data       #############################
###########################                       #############################

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()

from datetime import datetime
import datetime as dt


readRDS = robjects.r['readRDS']
df = readRDS(path + '/Jun-Dec19.rds')
df.to_pickle(path + '/TrishulData.pickle')

df = pd.read_pickle(path + '/Pickle Files/TrishulData.pickle')

df.columns = df.columns.str.replace('.','_')
df.columns = df.columns.str.title()
df = df.rename(columns = {'Sum([Pob_Value])' : 'Value', 'Sum([Ordered_Qty])' : 'Order_Qty'})
df['Date'] = df.Date.astype(int)

df['Date'] = df['Date'].apply(dt.datetime.fromordinal)
df['Month'] =  df['Date'].map(lambda x : x.month)
df['Year'] = 2019

temp = df[['Month','Year']].drop_duplicates().reset_index().drop(columns = ['index'])
arr = np.array([])
for i in range(1,8):
    arr = np.append(arr,i)
temp['Month_Order'] = pd.DataFrame(arr)
temp['Month_Order'] = temp.Month_Order.astype(int)

df = pd.merge(df,temp, on = ['Month','Year'], how = 'left')


pob = df.groupby('Retailer_Code',as_index = False).Value.sum()
active_months = df.groupby('Retailer_Code',as_index = False).agg({'Month_Order':['min','nunique']})
last = df.Month_Order.max()

pob = pd.merge(pob, active_months, on = 'Retailer_Code' , how = 'left')
pob = pob.rename(columns = {('Month_Order','min') : 'Mo_min' , ('Month_Order', 'nunique') : 'Mo_unique_12'})
pob['Tenure'] = last - pob['Mo_min'] + 1
pob['Valpermonth_Trishul'] = pob.Value / pob.Tenure

branch = pd.merge(branch, pob[['Retailer_Code','Valpermonth_Trishul']], on = 'Retailer_Code', how = 'left').fillna(0)

branch = branch[['Retailer_Code','Colour','Area_Name', 'New_Cluster_Name','New_Position_Name', 'Branch', 'Category', 'Valpermonth_Shakti', 'Valpermonth_Trishul', 'Rotation', 'Q1','Q2', 'Q3','Trend', 'Lockdown Value', 'Lockdown Active']]
branch.to_excel(path + '/temp1.xlsx')

