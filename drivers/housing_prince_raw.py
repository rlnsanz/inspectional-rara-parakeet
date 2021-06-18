import altair as alt
import dbfread
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

alt.data_transformers.enable('json')
alt.renderers.enable('mimetype')

dbf = dbfread.DBF(
"../property_example/L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf")
dbf = iter(dbf)
assets = pd.DataFrame(dbf)

sns.relplot(data=assets,
            x="YEAR_BUILT", y="BLDG_VAL", size='LOT_SIZE')

def get_threshold():
    return 1970

def is_new(col):
    return col > get_threshold()

assets['is_new'] = is_new(assets['YEAR_BUILT'])

clf = RandomForestClassifier(random_state=0)
y = assets['is_new']
x = assets[['BLDG_VAL', 'LOT_SIZE', 'NUM_ROOMS']]

clf.fit(x, y)
p = clf.predict([[100 * 1000, 10, 4]])
