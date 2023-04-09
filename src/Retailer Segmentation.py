
print('Retailer Segmentation.py started executing')
start = timeit.default_timer()

# =============================================================================
#           DATA PREPROCESSING FOR RETAILER SEGMENTATION
# =============================================================================

# global variable retailer being used (created in Retailer File.py)
retail = retailer[['Retailer_Code','Categ','Avg_Monthly_POB','Months_Since_LP','Brands_Percent','Active_Months','Declining_POB']].copy()
non_chemist = retail[retail.Categ == 'Non-Chemist'].reset_index().drop(columns = ['index'])
non_chemist = non_chemist[['Retailer_Code','Categ','Avg_Monthly_POB','Months_Since_LP','Brands_Percent','Active_Months','Declining_POB']]

chemist = retail[retail.Categ == 'Chemist'].reset_index().drop(columns = ['index'])

# global var recent being used(created in Retailer File.py)

chemist = chemist[~chemist.Retailer_Code.isin(recent.Retailer_Code)]
chemist['Declining_POB'] = np.where(np.isinf(chemist['Declining_POB']),np.nan,chemist['Declining_POB'])
chemist = chemist.dropna()
chemist = chemist.reset_index().drop(columns = ['index'])
retail1 = chemist[['Avg_Monthly_POB','Months_Since_LP','Brands_Percent','Active_Months','Declining_POB']].copy()
#retail1.to_pickle(path + '/Pickle Files/Retailer_Final.pickle')

# =============================================================================
#                      GAUSSIAN MIXTURE MODEL
# =============================================================================

# Imputer to deal with missing values
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean',verbose=0)
imputer = imputer.fit(retail1.iloc[:, 0:2])
retail1.iloc[:, 0:2] = imputer.transform(retail1.iloc[:, 0:2])

# To read retailers to be clustered for later use
#retail1 = pd.read_pickle('Retailer_Final.pickle')

# =============================================================================
#         GMM TRAINED MODEL OBJECT STORED IN Clustering Model.sav
# =============================================================================

#retail1 = retail1.dropna()
#gmm = GaussianMixture(n_components= 7, random_state = 9).fit(retail1)
#pickle.dump(gmm, open(filename, 'wb'))

# =============================================================================
# LOADING TRAINED MODEL OBJECT AND PREDICTING CLUSTERS FOR NEW DATA
# =============================================================================

filename = path + '/Pickle Files/Clustering Model.sav'
gmm = pickle.load(open(filename, 'rb'))

labels = gmm.predict(retail1)
probs = pd.DataFrame(gmm.predict_proba(retail1))
chemist['Segment_GMM'] = probs.idxmax(axis = 1)
non_chemist['Segment_GMM'] = 7

# =============================================================================
#           CLUSTER PROFILING FOR OLD CHEMISTS AND NON-CHEMISTS
# =============================================================================

z = chemist.groupby('Segment_GMM', as_index = False).mean()[['Avg_Monthly_POB','Months_Since_LP','Brands_Percent','Active_Months','Declining_POB']]
z['Size'] = chemist.groupby('Segment_GMM', as_index = False).size()
z = z.sort_values('Avg_Monthly_POB',ascending = False)
z = z.reset_index().rename(columns = {'index' : 'Segment'})
z['Percent'] = (z.Size/z.Size.sum())

# =============================================================================
#                   CLUSTER ASSIGNMENT FOR NEW CHEMISTS 
# =============================================================================

recent = recent[['Retailer_Code','Categ','Avg_Monthly_POB','Months_Since_LP','Brands_Percent','Active_Months','Declining_POB']].reset_index().drop(columns = ['index'])
item = []
for i in range(len(recent)):
    mi = 10000
    for j in range(len(z)):
        diff = abs(recent['Avg_Monthly_POB'][i] - z['Avg_Monthly_POB'][j])
        if (diff < mi):
            mi = diff
            seg = z['Segment'][j]
    item.append(seg)
    
recent['Segment_GMM'] = item

# =============================================================================
# FINALLY MERGING CLUSTERS FOR ALL RETAILERS TO Retailer DATAFRAME & ASSIGNING COLOURS
# =============================================================================

a = chemist.append(non_chemist, ignore_index = True)
a = a.append(recent, ignore_index = True)

retailer = pd.merge(retailer,a[['Retailer_Code','Segment_GMM']], on = 'Retailer_Code', how = 'left')
retailer['Colour'] = np.where(retailer['Segment_GMM'] == 6, 'Green', np.where(retailer['Segment_GMM'] == 3,'Light Amber',np.where(retailer['Segment_GMM'] == 1,'Deep Amber', '')))
retailer['Colour'] = np.where(retailer['Segment_GMM'] == 0, 'Red', np.where(retailer['Segment_GMM'] == 4 ,'Red',np.where(retailer['Segment_GMM'] == 2,'Red', retailer['Colour'])))
retailer['Colour'] = np.where(retailer['Segment_GMM'] == 5, 'Deep Red', np.where(retailer['Segment_GMM'] == 7,'Gray',retailer['Colour']))



