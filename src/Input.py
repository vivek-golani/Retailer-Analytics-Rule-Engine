
print('Input.py started executing')
start = timeit.default_timer()

# =============================================================================
#	     	READING SHAKTI DVL'S PICKLE FILE IF ITS NOT UPDATED
# =============================================================================

dvl_shakti = pd.read_pickle(path + '/Pickle Files/Updated_DVL.pickle')


# =============================================================================
#	     	     RUN ONLY IF SHAKTI DVL HAS BEEN UPDATED
# =============================================================================

#dvl_shakti = pd.read_excel(path + '/Input/Shakti DVL ' + month + "'" + str(year) + '.xlsx')
#dvl_shakti.columns = dvl_shakti.columns.str.replace(' ','_')
#dvl_shakti.columns = dvl_shakti.columns.str.title()
#dvl_shakti = dvl_shakti.rename(columns = {month + '_Retailer_Code' : 'Retailer_Code', month + '_Retailer_Name' : 'Retailer_Name'})
#dvl_shakti.to_pickle(path + '/Pickle Files/Updated_DVL.pickle')


# =============================================================================
#   INPUTTING DATA ONLY IF CREATING LAST MONTH FILE ELSE USE JUST PICKLE FILES
# =============================================================================

one_month_ago = datetime.datetime.now() - relativedelta(months=1)

#Inputting last month Retailer Transaction Report(POB File)
if(monthinteger == one_month_ago.month and year == one_month_ago.year):
	print('Accepting Inputs')
	df = pd.read_excel(path + "/Input/Retailer Transaction Report " + month + "'" + str(year) + ".xlsx", sheet_name='Sheet1')
	df['Month'] = monthinteger
	df['Year'] = year
	df.columns = df.columns.str.replace(' ','_')
	df.columns = df.columns.str.title()
	df['Category'] = df['Category'].str.title()
	df['Category'] = np.where(df['Category'] == 'Cosmetic','Cosmetics',df['Category'])
	df = df.rename(columns = {'Route_Name':'Beat_Code'})
	df = pd.merge(df,dvl_shakti[['Beat_Code','Beat_Name']].drop_duplicates(), on = 'Beat_Code', how = 'left')
	print('Retailer Transaction Report ' + month + "'" + str(year) + '.xlsx has been inputted')
	
	#Inputting last month Secondary File
	dfs = pd.read_excel(path + '/Input/Secondary Shakti ' + month + "'" + str(year) + '.xlsx')
	dfs['Month'] = monthinteger
	dfs['Year'] = year
	dfs.columns = dfs.columns.str.replace(' ','_')
	dfs.columns = dfs.columns.str.title()
	dfs = dfs.rename(columns = {'Sum([Secondary_Sales_Value])' : 'Value'})
	print('Secondary Shakti ' + month + "'" + str(year) + '.xlsx has been inputted')
   
	#Inputting last month compact pob file
	dfp = pd.read_excel(path + '/Input/Ret POB ' + month + "'" + str(year) + '.xlsx')
	dfp['Month'] = monthinteger
	dfp['Year'] = year
	dfp.columns = dfp.columns.str.replace(' ','_')
	dfp.columns = dfp.columns.str.title()
	dfp = dfp.rename(columns = {'Sum([Pob_Value])' : 'Value'})
	print('Ret POB ' + month + "'" + str(year) + '.xlsx has been inputted')


# =============================================================================
# CHOOSING WHICH HALF DOES ENTERED MONTH BELONG TO & APPENDING ENTERED MONTH DATA IF REQD.
# =============================================================================

h = 'h1' if monthinteger < 7 else 'h2'
half_pob = 'pob_' + h + '_' + str(year) + '.pickle'
half_sec ='sec_' + h + '_' + str(year) + '.pickle'
half_ret = 'ret_' + h + '_' + str(year) + '.pickle'

if(monthinteger == one_month_ago.month and year == one_month_ago.year): 
	if(monthinteger != 1 and monthinteger != 7):
		data2 = pd.read_pickle(path + '/Pickle Files/' + half_pob)
		sec2 = pd.read_pickle(path + '/Pickle Files/' + half_sec)
		pob2 = pd.read_pickle(path + '/Pickle Files/' + half_ret)
	else:
		data2 = pd.DataFrame()
		sec2 = pd.DataFrame()
		pob2 = pd.DataFrame()
        
	data2 = data2.append(df, ignore_index = True)
	data2 = data2.drop_duplicates()
	data2.to_pickle(path + '/Pickle Files/' + half_pob)
	sec2 = sec2.append(dfs, ignore_index = True)
	sec2 = sec2.drop_duplicates()
	sec2.to_pickle(path + '/Pickle Files/' + half_sec)
	pob2 = pob2.append(dfp, ignore_index = True)
	pob2 = pob2.drop_duplicates()
	pob2.to_pickle(path + '/Pickle Files/' + half_ret)

else:
    data2 = pd.read_pickle(path + '/Pickle Files/' + half_pob)
    sec2 = pd.read_pickle(path + '/Pickle Files/' + half_sec)
    pob2 = pd.read_pickle(path + '/Pickle Files/' + half_ret)
    data2 = data2[data2.Month <= monthinteger]
    sec2 = sec2[sec2.Month <= monthinteger]
    pob2 = pob2[pob2.Month <= monthinteger]

# Only for all_pob Dataframe
if(monthinteger < 6):
    half_ret = 'ret_h2_' + str(year-1) + '.pickle'
else :
    half_ret = 'ret_h1_' + str(year) + '.pickle'
        
pob1 = pd.read_pickle(path + '/Pickle Files/' + half_ret)

# =============================================================================
# CHOOSING THE OTHER HALF FILE FOR TOTAL 6 MONTHS DATA
# =============================================================================

if(monthinteger == 6 or monthinteger == 12):
    all_data = data2
    sec = sec2
    all_pob = pob1.append(pob2)
else :
    if(monthinteger < 6):
        half_pob = 'pob_h2_' + str(year-1) + '.pickle'
        half_sec = 'sec_h2_' + str(year-1) + '.pickle'
        half_ret = 'ret_h1_' + str(year-1) + '.pickle'
    else :
        half_pob = 'pob_h1_' + str(year) + '.pickle'
        half_sec = 'sec_h1_' + str(year) + '.pickle'
        half_ret = 'ret_h2_' + str(year-1) + '.pickle'
    
    data1 = pd.read_pickle(path + '/Pickle Files/' + half_pob)
    rem = 6 - (monthinteger - int(data2.Month.min()) + 1)
    data1 = data1[data1.Month > (data1.Month.max() - rem)]
    all_data = data1.append(data2, ignore_index = True)
    
    sec1 = pd.read_pickle(path + '/Pickle Files/' + half_sec)
    sec1 = sec1[sec1.Month > (sec1.Month.max() - rem)]
    sec = sec1.append(sec2, ignore_index = True)
    
    pob0 = pd.read_pickle(path + '/Pickle Files/' + half_ret)
    pob0 = pob0[pob0.Month > (pob0.Month.max() - rem)]
    all_pob = pob0.append(pob1, ignore_index = True)
    all_pob = all_pob.append(pob2, ignore_index = True)

all_data = all_data.sort_values(['Year','Month'])
sec = sec.sort_values(['Year','Month'])
all_pob = all_pob.sort_values(['Year','Month'])

all_data = all_data.drop_duplicates()
sec = sec.drop_duplicates()
all_pob = all_pob.drop_duplicates()

# =============================================================================
#                   QC Statements- Uncomment to check
# =============================================================================

# all_data.Month.unique()
# sec.Month.unique()
# all_pob.Month.unique()


# =============================================================================
# ADDING Month_Order COLUMN IN ALL DATAFRAMES FOR EASE IN L3M, L456M CALCULATIONS
# =============================================================================

all_data = all_data[~pd.isna(all_data.Month)]

temp = all_data[['Month','Year']].drop_duplicates().reset_index().drop(columns = ['index'])
arr = np.array([])
for i in range(1,7):
    arr = np.append(arr,i)
temp['Month_Order'] = pd.DataFrame(arr)
temp['Month_Order'] = temp.Month_Order.astype(int)

all_data = pd.merge(all_data,temp, on = ['Month','Year'], how = 'left')
sec = pd.merge(sec,temp, on = ['Month','Year'], how = 'left')


temp = all_pob[['Month','Year']].drop_duplicates().reset_index().drop(columns = ['index'])
arr = np.array([])
for i in range(1,13):
    arr = np.append(arr,i)
temp['Month_Order'] = pd.DataFrame(arr)
temp['Month_Order'] = temp.Month_Order.astype(int)
all_pob = pd.merge(all_pob,temp, on = ['Month','Year'], how = 'left')

# =============================================================================
#                   QC Statements- Uncomment to check
# =============================================================================

# all_data.Month_Order.unique() #1-6
# sec.Month_Order.unique()      #1-6
# all_pob.Month_Order.unique()  #1-12


# =============================================================================
# REMOVING UNWANTED DATAFRAMES TO REDUCE RAM USAGE
# =============================================================================

if(monthinteger == 6 or monthinteger == 12):
    del data2,sec2,pob1,pob2
else:
    del data1,data2,sec1,sec2,pob0,pob1,pob2