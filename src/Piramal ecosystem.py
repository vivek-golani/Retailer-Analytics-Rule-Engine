
# =============================================================================
#           CREATING DATAFRAME(y) FOR PROFILING OF RETAILERS
# =============================================================================

y = retailer.groupby('Colour').mean()[['Avg_Monthly_POB','Months_Since_LP','Brands_Percent','Active_Months','Declining_POB']]
y['Size'] = retailer.groupby('Colour').size()
y['Net_Monthly_POB'] = retailer.groupby('Colour').Avg_Monthly_POB.sum()
y['POB_Percent'] = (y.Net_Monthly_POB/y.Net_Monthly_POB.sum())

branch = pd.read_pickle(path + '/Pickle Files/Branches.pickle')
branch = branch[~pd.isna(branch.Branch)]
branch = pd.merge(branch,retailer[['Retailer_Code','Colour']], on = 'Retailer_Code', how = 'left')
y['Branch'] = branch.groupby('Colour').size()

y = y.sort_values('Avg_Monthly_POB',ascending = False)
y = y.reset_index().rename(columns = {'index' : 'Segment'})
y['Percent'] = (y.Size/y.Size.sum())

# =============================================================================
#   FORMATTING THE DATAFRAME FOR PROFILING OF RETAILERS(FINAL DF = re)
# =============================================================================

re = pd.DataFrame(['Green','Light Amber','Deep Amber','Red','Deep Red','Gray'], columns = ['Colour'])
re = pd.merge(re,y, on = 'Colour', how = 'left')
re = re[['Size','Percent','Net_Monthly_POB','POB_Percent','Avg_Monthly_POB','Active_Months','Months_Since_LP','Declining_POB','Brands_Percent','Branch']]

# =============================================================================
#       DATAFRAME FOR TOTAL ROW(tot) OF PROFILING OF RETAILERS
# =============================================================================

tot = retailer[['Avg_Monthly_POB','Months_Since_LP','Brands_Percent','Active_Months','Declining_POB']].mean()
tot['Size'] = y.Size.sum()
tot['Net_Monthly_POB'] = y.Net_Month_POB.sum()
tot['POB_Percent'] = 1
tot['Percent'] = 1
tot = tot[['Size','Percent','Net_Monthly_POB','POB_Percent','Avg_Monthly_POB','Active_Months','Months_Since_LP','Declining_POB','Brands_Percent']]

# =============================================================================
#               PRINTING FOR PROFILING OF RETAILERS
# =============================================================================

app = xw.App()
book = xw.Book(path  + "/Templates/Piramal Ecosystem Retailers.xlsx")
sheet1 = book.sheets('Retailers')
sheet2 = book.sheets('Branches')

book.sheets[sheet1].range('C11:L' + str(re.shape[0] + 10)).value = np.array(re)    
book.sheets[sheet1].range('C17:K' + str(tot.shape[0] + 16)).value = np.array(tot)    

book.save(path + '/Output/Piramal Ecosystem Retailers - ' + month + '.xlsx')
book.close()
app.kill()
