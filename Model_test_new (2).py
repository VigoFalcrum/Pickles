import numpy as np
import pyarrow
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import pickle
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import time
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import xgboost as xgb

datatypes = {'srcip' : int, 'sport' : int, 'dstip' : int, 'dsport' : int, 'proto' : int, 'state' : int, 'dur' : float, \
             'sbytes' : int, 'dbytes' : int, 'sttl' : int, 'dttl' : int, 'sloss' : int, 'dloss' : int, 'service' : int, \
             'Sload' : float, 'Dload' : float, 'Spkts' : int, 'Dpkts' : int, 'swin' : int, 'dwin' : int, 'stcpb' : int, \
             'dtcpb' : int, 'smeansz' : int, 'dmeansz' : int, 'trans_depth' : int, 'res_bdy_len' : int, 'Sjit' : float, \
             'Djit' : float, 'Sintpkt' : float, 'Dintpkt' : float, 'tcprtt' : float, \
             'synack' : float, 'ackdat' : float, 'is_sm_ips_ports' : int, 'ct_state_ttl' : int, 'ct_flw_http_mthd' : int, \
             'ct_srv_src' : int, 'ct_srv_dst' : int, 'ct_dst_ltm' : int, \
             'ct_src_ltm' : int, 'ct_src_dport_ltm' : int, 'ct_dst_sport_ltm' : int, 'ct_dst_src_ltm' : int}

col_names = ['srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', \
             'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', \
             'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', \
             'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'ct_srv_src', \
             'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm']

X_test_data = 'X_test.csv'
y_test_data = 'y_test.csv'

X_test = pd.read_csv(X_test_data, header = 0, dtype = datatypes)
y_test = pd.read_csv(y_test_data, header = 0, dtype = datatypes)

X_test.columns = col_names
y_test.columns = ['label']

X_test = X_test.drop(X_test.index[0])
y_test = y_test.drop(y_test.index[0])

#for col in X_test.columns:
#    temp = X_test[col].iloc[0]
#    if type(temp) == np.int64:
#        X_test[col] = X_test[col].astype('int')
#    elif type(temp) == np.float64:
#        X_test[col] = X_test[col].astype('float')

with open('RF_80_15_1500.pkl', 'rb') as file:
	clf = pickle.load(file)

for i in range(0, 10):
	y_pred = clf.predict(X_test)

y_test = y_test.astype('int64')
print('Model accuracy score with criterion entropy: {0:0.4f}'. format(accuracy_score(y_test, y_pred)))
