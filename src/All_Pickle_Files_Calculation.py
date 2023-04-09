

#reading Shakti DVL list 
dvl_shakti = []
with open_xlsb(path + '/Input/Shakti_DVL' + month + '.xlsb') as wb:
    with wb.get_sheet(1) as sheet:
        for row in sheet.rows():
            dvl_shakti.append([item.v for item in row])

dvl_shakti = pd.DataFrame(dvl_shakti[1:], columns=dvl_shakti[0])
dvl_shakti.columns = dvl_shakti.columns.str.replace(' ','_')
dvl_shakti.columns = map(str.title, dvl_shakti.columns)
dvl_shakti = dvl_shakti.rename(columns = {'New_Retailer_Code' : 'Retailer_Code', 'New_Retailer_Name' : 'Retailer_Name'})
dvl_shakti = pd.merge(dvl_shakti, update[['Retailer_Code','New_Cluster_Code','New_Cluster_Name','New_Position_Code','New_Position_Name']], left_on = 'Retailer_Code', right_on = 'Retailer_Code', how = 'left')
dvl_shakti.to_pickle(path + '\Pickle Files\Updated_DVL.pickle')
#dvl_shakti = dvl_shakti.drop(columns = ['New_Cluster_Code_x','New_Cluster_Code_y','New_Cluster_Name_x','New_Cluster_Name_y','New_Position_Code_x','New_Position_Code_y','New_Position_Name_x','New_Position_Name_y'])


# =============================================================================
#   	NOT TO BE USED, HAD BEEN USED FOR INITIAL CALCULATIONS 
# =============================================================================


#appending pob data of last 6 months in all_data
all_data = pd.DataFrame()
for f in glob.glob(path + "/Input/Retailer_Transaction_Report*.xlsx"):
    df = pd.read_excel(f, sheet_name='Sheet1')
    all_data = all_data.append(df,ignore_index=True)

all_data.columns = all_data.columns.str.replace(' ','_')
all_data.columns = map(str.title(),all_data.columns)
all_data = all_data.sort_values('Week')
all_data['Date_Of_Work'] = pd.to_datetime(all_data['Date_Of_Work'])
all_data['Month'] = pd.DatetimeIndex(all_data.DATE_OF_WORK).month
all_data['Categ'] = np.where(all_data['Category'] == 'Medical', 'Chemist', 'Non-Chemist')


#secondary data in sec
sec = pd.read_excel(path + '/Input/secondary_data.xlsx')
sec.columns = map(str.title, sec.columns)
sec.columns = sec.columns.str.replace(' ','_')
#sec = sec.rename(columns = {'Zone Name' : 'Zone_Name','Area Code': 'Area_Code','Area_Name' : 'Area_Name','Cluster Name':'Cluster_Name', 'Cluster Code' : 'Cluster_Code','Fiscal Month Year' : 'Fiscal_Month_Year', 'Sum([Secondary Sales Value])' : 'Value'})
item = []
for i in range(len(sec)):
    item.append(datetime.datetime.strptime(sec['Fiscal_Month_Year'][i],'%b-%y').month)
sec['Month'] = item
sec.to_pickle(path + '\Pickle Files\Secondary_Jun_Nov.pickle')
sec = pd.merge(sec, update)


#all pob data for 1 year Jan-Dec 19
all_pob  = pd.DataFrame()
for f in glob.glob(path + "\Input\POB\Ret_POB_Q*.xlsx"):
    df = pd.read_excel(f, sheet_name='Sheet1')
    all_pob = all_pob.append(df,ignore_index=True)
all_pob = all_pob.rename(columns = {'FISCAL MONTH YEAR' : 'FISCAL_MONTH_YEAR'})
all_pob.columns = all_pob.columns.str.replace(' ','_')
all_pob.columns = map(str.title, all_pob.columns)
all_pob.to_pickle(path + '\Pickle Files\All_POB.pickle')

