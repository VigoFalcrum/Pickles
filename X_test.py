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
import time

raw_data1 = 'UNSW-NB15_1.csv'
raw_data2 = 'UNSW-NB15_2.csv'
raw_data3 = 'UNSW-NB15_3.csv'
raw_data4 = 'UNSW-NB15_4.csv'

col_names = ['srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', \
             'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz', 'dmeansz', \
             'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', \
             'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', \
             'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat', \
             'Label']

datatypes = {'srcip' : str, 'sport' : int, 'dstip' : str, 'dsport' : int, 'proto' : str, 'state' : str, 'dur' : float, \
             'sbytes' : int, 'dbytes' : int, 'sttl' : int, 'dttl' : int, 'sloss' : int, 'dloss' : int, 'service' : str, \
             'Sload' : float, 'Dload' : float, 'Spkts' : int, 'Dpkts' : int, 'swin' : int, 'dwin' : int, 'stcpb' : int, \
             'dtcpb' : int, 'smeansz' : int, 'dmeansz' : int, 'trans_depth' : int, 'res_bdy_len' : int, 'Sjit' : float, \
             'Djit' : float, 'Stime' : str, 'Ltime' : str, 'Sintpkt' : float, 'Dintpkt' : float, 'tcprtt' : float, \
             'synack' : float, 'ackdat' : float, 'is_sm_ips_ports' : int, 'ct_state_ttl' : int, 'ct_flw_http_mthd' : int, \
             'is_ftp_login' : int, 'ct_ftp_cmd' : int, 'ct_srv_src' : int, 'ct_srv_dst' : int, 'ct_dst_ltm' : int, \
             'ct_src_ltm' : int, 'ct_src_dport_ltm' : int, 'ct_dst_sport_ltm' : int, 'ct_dst_src_ltm' : int, \
             'attack_cat' : str, 'Label' : int}

UNSW_data1 = pd.read_csv(raw_data1, header = None, dtype = datatypes)
UNSW_data2 = pd.read_csv(raw_data2, header = None, dtype = datatypes)
UNSW_data3 = pd.read_csv(raw_data3, header = None, dtype = datatypes)
UNSW_data4 = pd.read_csv(raw_data4, header = None, dtype = datatypes)

UNSW_data = pd.concat([UNSW_data1, UNSW_data2, UNSW_data3, UNSW_data4], ignore_index = True)
#UNSW_data = UNSW_data1

UNSW_data.columns = col_names
UNSW_data.fillna(0, inplace = True)
UNSW_data = UNSW_data.drop(['Stime', 'Ltime', 'is_ftp_login', 'ct_ftp_cmd', 'attack_cat'], axis = 1)
# Isolate the first 8 bits of the IP addresses
datasize = UNSW_data.shape[0]

for i in range(0, datasize):
    if i % 50000 == 0:
        percent = i/datasize*100
        print(f"{percent:.1f}%\n")
    
    # Source IP
    temp = UNSW_data.at[i, 'srcip']
    if temp[3] == '.':
        UNSW_data.at[i, 'srcip'] = int(temp[0 : 3])
    else:
        UNSW_data.at[i, 'srcip'] = int(temp[0 : 2])
    
    # Destination IP
    temp = UNSW_data.at[i, 'dstip']
    if temp[3] == '.':
        UNSW_data.at[i, 'dstip'] = int(temp[0 : 3])
    else:
        UNSW_data.at[i, 'dstip'] = int(temp[0 : 2])

print("100.0%")

# Encode categorical features
UNSW_data['proto'], _ = pd.factorize(UNSW_data['proto'])
UNSW_data['state'], _ = pd.factorize(UNSW_data['state'])
UNSW_data['service'], _ = pd.factorize(UNSW_data['service'])

dtype_counts_per_column = {}
df = UNSW_data
for col in df.columns:
    dtype_counts_per_column[col] = df[col].apply(type).nunique()

print("Number of different data types in each column:")
print(dtype_counts_per_column)

# dsport column contains some corrupt data, which is most likely in hex (all corrupt entries contain 0xcc09, which is
# 3273 in hex) - we must properly convert these into ints to proceed

counter = 0
weirdos = ['string'] * 7

for i in range (0, datasize):
    temp = UNSW_data.at[i, 'dsport']
    try:
        UNSW_data.at[i, 'dsport'] = int(UNSW_data.at[i, 'dsport'])
    except ValueError:
        if temp == '0x20205321':
            UNSW_data.at[i, 'dsport'] = 538989345
        elif temp == '0xcc09':
            UNSW_data.at[i, 'dsport'] = 52233
        elif temp == '0xc0a8':
            UNSW_data.at[i, 'dsport'] = 49320
        elif temp == '-':
            UNSW_data.at[i, 'dsport'] = 0
        else:
            weirdos[counter] = temp
            counter += 1

# counter = 0 indicates a successful conversion
print(counter)
print("\n") 
for weirdo in weirdos:
    print(weirdo)
    print()

# sport column contains some corrupt data, which is most likely in hex (all corrupt entries contain 0xcc09, which is
# 3273 in hex) - we must properly convert these into ints to proceed

counter = 0
weirdos = ['string'] * 8

for i in range (0, datasize):
    temp = UNSW_data.at[i, 'sport']
    try:
        UNSW_data.at[i, 'sport'] = int(UNSW_data.at[i, 'sport'])
    except ValueError:
        if temp == '0x000b':
            UNSW_data.at[i, 'sport'] = 11
        elif temp == '0x000c':
            UNSW_data.at[i, 'sport'] = 12
        elif temp == '-':
            UNSW_data.at[i, 'sport'] = 0
        else:
            weirdos[counter] = temp
            counter += 1

# counter = 0 indicates a successful conversion
print(counter)
print("\n") 

# Create the test and train datasets
# Run to use a different classifier

X = UNSW_data.drop(['Label'], axis = 1)
y = UNSW_data.Label
# 75 25 is the standard
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 29)
X_test.to_csv('X_test.csv', index = False)
y_test.to_csv('y_test.csv', index = False)
X_train.to_csv('X_train.csv', index = False)
y_train.to_csv('y_train.csv', index = False)