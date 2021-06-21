import numpy as np
import pandas as pd

datadir = '/kaggle/input/shopee-code-league-20/_DA_Logistics/delivery_orders_march.csv'
data = pd.read_csv(datadir)

# inspecting data
data.head()

# any missing values? what types of data?
data.info()

# get the state of the address by getting the last str in the address
data['buyeraddress'] = data['buyeraddress'].apply(lambda x: x.split()[-1]).str.lower()
data['selleraddress'] = data['selleraddress'].apply(lambda x: x.split()[-1]).str.lower()
data.head()

# calculate the business days to deliver before late 
temp = []
for i,j in data[['buyeraddress','selleraddress']].itertuples(index=False):
  if (i == 'manila' and j == 'manila'):
    temp.append(3)
  elif (
      (i == 'manila' and j == 'luzon')
      or (i == 'luzon' and j == 'manila')
      or (i == 'luzon' and j == 'luzon')
      ):
    temp.append(5)
  else:
    temp.append(7)

data['days'] = temp
data.head()

# change unix time to date
# need to convert to gmt+8
data[['pick','1st_deliver_attempt','2nd_deliver_attempt']] += 8*60*60
data['pick'] = pd.to_datetime(data['pick'],unit='s').dt.date
data['1st_deliver_attempt'] = pd.to_datetime(data['1st_deliver_attempt'],unit='s').dt.date
data['2nd_deliver_attempt'] = data['2nd_deliver_attempt'].replace(np.nan,0) # change nan to 0 or else can't be process
data['2nd_deliver_attempt'] = pd.to_datetime(data['2nd_deliver_attempt'],unit='s').dt.date
data.head()

# count how many days of business day taken for the 1pick and 2pick
holiday = ['2020-03-08','2020-03-25','2020-03-30','2020-03-31']

data['1st_pick'] = np.busday_count(data['pick'], data['1st_deliver_attempt'], weekmask='1111110', holidays=holiday)
data['2nd_pick'] = np.busday_count(data['1st_deliver_attempt'], data['2nd_deliver_attempt'] , weekmask='1111110', holidays=holiday)
data.head()

# check if is late
data['is_late'] = (data['1st_pick'] > data['days']) | (data['2nd_pick'] > 3)
data.head()

# prepare submission df and change is_late column to int using .apply(int)
submission = pd.DataFrame({'orderid':data['orderid'], 'is_late':data['is_late'].apply(int)})
submission

submission.to_csv('submission.csv', header=True, index=False)