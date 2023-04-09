
print('Report.py started executing')

# =============================================================================
#   Input.py READS INPUT FILES AND CREATES DATAFRAMES FOR 6 MONTH DATA
# =============================================================================

filename = path + "/Codes/Input.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))
stop = timeit.default_timer()   
print('Input.py ran successfully in ' + str(round(stop - start)) + ' seconds')

# =============================================================================
#   Update.py UPDATES ALL POSITIONS, CLUSTERS AND AREA ACC. TO LAST MONTH
# =============================================================================

filename = path + "/Codes/Update.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))
stop = timeit.default_timer()   
print('Update.py ran successfully in ' + str(round(stop - start)) + ' seconds')

# =============================================================================
#   Cluster.py CREATES DATAFRAME FOR CLUSTER TAB
# =============================================================================

filename = path + "/Codes/Cluster File.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))
stop = timeit.default_timer()   
print('Cluster File.py ran successfully in ' + str(round(stop - start)) + ' seconds')

# =============================================================================
#   Position.py CREATES DATAFRAME FOR POSITION TAB
# =============================================================================

filename = path + "/Codes/Position File.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))
stop = timeit.default_timer()   
print('Position File.py ran successfully in ' + str(round(stop - start)) + ' seconds')


# =============================================================================
#   Beat.py CREATES DATAFRAME FOR BEAT TAB
# =============================================================================

filename = path + "/Codes/Beat File.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))
stop = timeit.default_timer()   
print('Beat File.py ran successfully in ' + str(round(stop - start)) + ' seconds')

# =============================================================================
#   Retailer.py CREATES DATAFRAME FOR RETAILER TAB
# =============================================================================

filename = path + "/Codes/Retailer File.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))
stop = timeit.default_timer()   
print('Retailer File.py ran successfully in ' + str(round(stop - start)) + ' seconds')


# =============================================================================
#   Retailer Segmentation.py FOR PREDICTING RETAILER CLUSTERS
# =============================================================================

filename = path + "/Codes/Retailer Segmentation.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))
stop = timeit.default_timer()   
print('Retailer Segmentation.py ran successfully in ' + str(round(stop - start)) + ' seconds')

# =============================================================================
#   Print.py FOR PRINTING FOR ALL AREAS
# =============================================================================

filename = path + "/Codes/Print.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))
stop = timeit.default_timer()   
print('Print.py ran successfully in ' + str(round((stop - start)/60)) + ' minutes')

print('Report.py ran successfully')
