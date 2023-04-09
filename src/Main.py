
# =============================================================================
#                   IMPORTING CONCERNED LIBRARIES
# =============================================================================

from __future__ import print_function
import os
import glob
import pickle
import timeit
import os.path
import unittest
import easygui
import warnings
import datetime
import numpy as np
import pandas as pd
import xlwings as xw
import win32com.client
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans
from dateutil.relativedelta import *
from sklearn.mixture import GaussianMixture
from pyxlsb import open_workbook as open_xlsb
from xlwings.constants import DeleteShiftDirection
from sklearn.preprocessing import StandardScaler, normalize 


# =============================================================================
#               GETTING THE CURRENT WORKING DIRECTORY
# =============================================================================

path = os.getcwd()

# =============================================================================
#                   INPUTTING MONTH AND YEAR 
# =============================================================================

# enter month no. as single digit. Ex: 2,3 etc
monthinteger = easygui.enterbox("Enter month number")
monthinteger = int(monthinteger)
month = datetime.date(2020, monthinteger, 1).strftime('%b')
year = easygui.enterbox("Enter year in yyyy format")
year = int(year)


# =============================================================================
#            CALLING Report.py WHICH CALLS ALL OTHER SCRIPTS
# =============================================================================

filename = path + "/Codes/Report.py"
exec(compile(open(filename, "rb").read(), filename, 'exec'))

