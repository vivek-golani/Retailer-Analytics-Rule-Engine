
print('Print.py started executing')
start = timeit.default_timer()

# =============================================================================
#                          PRINTING FOR ALL AREAS
# =============================================================================
area_array = all_data.New_Area_Code.unique()

for ar in area_array:
    
    area = all_data[all_data.New_Area_Code == ar].New_Area_Name.unique()[0]

# =============================================================================
# CREATING clus, pos, be, ret, ret_clus, clus_list and pos_list for each area 
# =============================================================================

    clus = cluster[cluster.New_Area_Code == ar].reset_index().drop(columns = ['index'])[['Zone_Name', 'New_Area_Name', 'New_Cluster_Name', 'Avg_Monthly_POB', 'Last_Month_POB', 'Last_Month_Sec', 'Declining_Sec','Total_Retailers','Chemist_Retailers','Last_Month_Retailers', 'Productivity','Avg_Brands','Avg_VPO','Last_Month_PC','Avg_VPC','Pob_Sec']]
    pos = position[position.New_Area_Code == ar].reset_index().drop(columns = ['index'])[['Zone_Name', 'New_Area_Name', 'New_Cluster_Name', 'New_Position_Code','New_Position_Name', 'Brand', 'Avg_Monthly_POB', 'Last_Month_POB', 'Declining_POB','Total_Retailers','Chemist_Retailers','Last_Month_Retailers', 'Productivity','Avg_Brands','Avg_VPO','Last_Month_PC','Avg_VPC']]
    be = beat[beat.New_Area_Code == ar].reset_index().drop(columns = ['index'])[['Zone_Name', 'New_Area_Name', 'New_Cluster_Name','Position','New_Beat_Name','Brand', 'Avg_Monthly_POB', 'Last_Month_POB', 'Declining_POB','Total_Retailers','Chemist_Retailers','Last_Month_Retailers', 'Productivity','Avg_Brands','Avg_VPO','Last_Month_PC','Avg_VPC']]
    ret = retailer[retailer.New_Area_Code == ar].reset_index().drop(columns = ['index'])[['Retailer_Code','Retailer_Name','Zone_Name','New_Area_Name','New_Cluster_Name','Position','New_Beat_Name','Categ','Brand','Avg_Monthly_POB','Last_Month_POB','Declining_POB','Months_Since_LP','Active_Months','Last_Month_PC','Avg_VPC']]
    
    #clustering of retailers sheet
    ret_clus = retailer[retailer.New_Area_Code == ar].reset_index().drop(columns = ['index'])[['Retailer_Code','Colour']]
    
    # cluster list sheet
    clus_list = all_data[all_data.New_Area_Code == ar].New_Cluster_Code.unique()
    
    #cluster position mapping sheet
    pos_list = pd.DataFrame([])
    
    for cl in clus_list:
        temp = pd.DataFrame(['All'],columns = ['Position'])
        temp1 = pd.DataFrame(all_data[all_data.New_Cluster_Code == cl].New_Position_Code.unique(), columns = ['Position_Code'])
        temp1['Position_Name'] = temp1['Position_Code'].map(lambda x : all_data[all_data.New_Position_Code == x].New_Position_Name.unique()[0])
        temp1['Position'] = temp1['Position_Code'].astype(str) + '-' + temp1['Position_Name']
        temp = temp.append(temp1, ignore_index = True)
        pos_list[cl] = temp['Position']
    
    clus_list = pd.DataFrame(clus_list)
    clus_list['Name'] = clus_list[0].map(lambda x : all_data[all_data.New_Cluster_Code == x].New_Cluster_Name.unique()[0])
    clus_list = clus_list.drop(columns = [0])   

    clus_trans = clus_list.transpose()
    
    temp = pd.DataFrame(index=range(0,2),columns = ['Position']) 
    temp['Position'] = 'All'
    
# =============================================================================
#                       PRINTING USING Xlwings 
# =============================================================================

    app = xw.App()
    book = xw.Book(path  + '/Templates/RARE_Template.xlsb')
    sheets = ['Cluster', 'Position', 'Beat', 'Retailer']
    extra = ['Clustering of Retailers','Cluster List']
    sheets_data = [clus, pos, be, ret]
    extra_data = [ret_clus, clus_list]
    
    st_mo = all_data[all_data.Month_Order == 1].Month.unique()[0]
    st_yr = all_data[all_data.Month_Order == 1].Year.unique()[0]
    m = datetime.date(2020, st_mo, 1).strftime('%b')
    period = m + '\'' + str(st_yr) + ' - ' + month + '\'' + str(year)
    
    book.sheets['Main'].range('D19').value = np.array(period)
    
    # Writing the data
    for i in range(len(sheets)):
        sh = sheets[i]
        sh_data = sheets_data[i]
        book.sheets[sh].range('B13:Q'+ str(sh_data.shape[0] + 12)).value = np.array(sh_data)
        book.sheets[sh].range(str(sh_data.shape[0] + 13) + ':1048576').api.Delete(DeleteShiftDirection.xlShiftUp)
    
    for i in range(len(extra)):
        sh = extra[i]
        sh_data = extra_data[i]
        book.sheets[sh].range('A2:B'+ str(sh_data.shape[0] + 2)).value = np.array(sh_data)
        book.sheets[sh].range(str(sh_data.shape[0] + 2) + ':1048576').api.Delete(DeleteShiftDirection.xlShiftUp)
    
    book.sheets['Cluster Position Map'].range('A1:B' + str(temp.shape[0])).value = np.array(temp)    
    book.sheets['Cluster Position Map'].range('B1:J' + str(clus_trans.shape[0])).value = np.array(clus_trans)
    book.sheets['Cluster Position Map'].range('B2:J' + str(pos_list.shape[0] + 1)).value = np.array(pos_list)
    book.sheets['Cluster Position Map'].range(str(pos_list.shape[0] + 2) + ':1048576').api.Delete(DeleteShiftDirection.xlShiftUp)
    
    
    # Save and close the sheet
    book.save(path + '/Output/RARE ' + area + ' - ' + month + '.xlsb')
    book.close()
    app.kill()
    
# =============================================================================
#     CALLING Run Macro.py FOR TRIGGERING CreateFromSelection MACRO
# =============================================================================
    
    filename = path + "/Codes/Run Macro.py"
    exec(compile(open(filename, "rb").read(), filename, 'exec'))