import gadget as ln
with ln.tracking('housing_price'):
    import altair as alt
    ln.importing(alt, module='altair', name='alt', line_no=1)
    import dbfread
    ln.importing(dbfread, module='dbfread', name='dbfread', line_no=2)
    import pandas as pd
    ln.importing(pd, module='pandas', name='pd', line_no=3)
    import seaborn as sns
    ln.importing(sns, module='seaborn', name='sns', line_no=4)
    from sklearn.ensemble import RandomForestClassifier
    ln.importing(RandomForestClassifier, module='sklearn.ensemble', name=
        'RandomForestClassifier', line_no=5)
    ln.call(alt.data_transformers.enable('json'), text=
        "alt.data_transformers.enable('json')", line_no=7)
    ln.call(alt.renderers.enable('mimetype'), text=
        "alt.renderers.enable('mimetype')", line_no=8)
    dbf = ln.call(dbfread.DBF(
        '../property_example/L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf'
        ), text=
        """dbfread.DBF(
    '../property_example/L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf')"""
        , line_no=10).assign(target='dbf')
    dbf = ln.call(iter(dbf), text='iter(dbf)', line_no=12).assign(target='dbf')
    assets = ln.call(pd.DataFrame(dbf), text='pd.DataFrame(dbf)', line_no=13
        ).assign(target='assets')
    ln.call(sns.relplot(data=assets, x='YEAR_BUILT', y='BLDG_VAL', size=
        'LOT_SIZE'), text=
        "sns.relplot(data=assets, x='YEAR_BUILT', y='BLDG_VAL', size='LOT_SIZE')"
        , line_no=15)

    def get_threshold():
        with ln.func(name='get_threshold', args=[], ret_text='(1970)',
            line_no=18):
            return 1970
    ln.assign(get_threshold, text='get_threshold', line_no=18, target=
        'get_threshold')

    def is_new(col):
        with ln.func(name='is_new', args=[(col, 'col')], ret_text=
            '(col > get_threshold())', line_no=21):
            return col > get_threshold()
    ln.assign(is_new, text='is_new', line_no=21, target='is_new')
    assets['is_new'] = ln.call(is_new(assets['YEAR_BUILT']), text=
        "is_new(assets['YEAR_BUILT'])", line_no=24).assign(target=
        "assets['is_new']")
    clf = ln.call(RandomForestClassifier(random_state=0), text=
        'RandomForestClassifier(random_state=0)', line_no=26).assign(target
        ='clf')
    y = ln.assign(assets['is_new'], text="assets['is_new']", line_no=27,
        target='y')
    x = ln.assign(assets[['BLDG_VAL', 'LOT_SIZE', 'NUM_ROOMS']], text=
        "assets[['BLDG_VAL', 'LOT_SIZE', 'NUM_ROOMS']]", line_no=28, target='x'
        )
    ln.call(clf.fit(x, y), text='clf.fit(x, y)', line_no=30)
    p = ln.call(clf.predict([[100 * 1000, 10, 4]]), text=
        'clf.predict([[100 * 1000, 10, 4]])', line_no=31).assign(target='p')