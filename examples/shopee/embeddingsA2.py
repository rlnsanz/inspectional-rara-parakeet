import numpy as np
import pandas as pd

orders = pd.read_csv('~/datas/_DA_Logistics/delivery_orders_march.csv')

orders.head()

orders.info()

orders.buyeraddress = orders.buyeraddress.apply(lambda x: x.split()[-1]).str.title()
orders.selleraddress = orders.selleraddress.apply(lambda x: x.split()[-1]).str.title()

orders.head()

print(orders.buyeraddress.unique())
print(orders.selleraddress.unique())

manila, luzon, visayas, mindano = orders.buyeraddress.unique()
cities = (manila, luzon, visayas, mindano)

orders['days_limit'] = [{(manila, manila): 3, (manila, luzon): 5, (luzon, manila): 5, (luzon, luzon): 5,}.get((s, b), 7)
                        for s,b in orders[['selleraddress', 'buyeraddress']].itertuples(index=False)]
orders.head()

time_features = ['pick', '1st_deliver_attempt', '2nd_deliver_attempt']

orders[time_features] += 8 * 60 * 60
orders['2nd_deliver_attempt'] = orders['2nd_deliver_attempt'].replace(np.nan, 0)
for f in time_features:
    orders[f] = pd.to_datetime(orders[f], unit = 's').dt.date
    
orders.head()

holidays = ['2020-03-25','2020-03-30','2020-03-31']

orders['1st_attempt_days'] = np.busday_count(orders['pick'], orders['1st_deliver_attempt'], weekmask = '1111110', holidays = holidays)
orders['2nd_attempt_days'] = np.busday_count(orders['1st_deliver_attempt'], orders['2nd_deliver_attempt'], weekmask = '1111110', holidays = holidays)

orders.head()


orders['is_late'] = (orders['1st_attempt_days'] > orders['days_limit']) | (orders['2nd_attempt_days'] > 3)

orders.head()

orders.is_late.value_counts()

# import matplotlib.pyplot as plt
#
# fig, ax = plt.subplots(figsize = (8, 8))
#
# ax = plt.pie(x = orders.is_late.value_counts(), labels = ['False', 'True'], explode = (0, 0.1), shadow = True, autopct = '%1.1f%%', startangle = 90)
# plt.title('Percent of orders with late deliveries')
# plt.show()