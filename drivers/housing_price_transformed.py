import gadget as ln
with ln.tracking('housing_price'):
    import altair as alt
    import dbfread
    import pandas as pd
    import seaborn as sns
    from sklearn.ensemble import RandomForestClassifier

    ln.importing(alt, module='altair', name='alt', line_no=1)
    ln.importing(dbfread, module='dbfread', name='dbfread', line_no=2)
    ln.importing(pd, module='pandas', name='pd', line_no=3)
    ln.importing(sns, module='seaborn', name='sns', line_no=4)
    ln.importing(RandomForestClassifier, module='sklearn.ensemble.RandomForestClassifier', name='RandomForestClassifier', line_no=5)

    # Set up some config
    # ln.call(pe=, text=, line_no=, args=)
    ln.call(alt.data_transformers.enable('json'), text="alt.data_transformers.enable('json')", line_no=6)
    ln.call(alt.renderers.enable('mimetype'), text="alt.renderers.enable('mimetype')", line_no=7)

    dbf = ln.call(dbfread.DBF("../../tracer/property_example/L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf"),
                  text='dbfread.DBF("./L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf")', line_no=8
                  ).assign(target='dbf')
    dbf = ln.call(iter(dbf), text='iter(dbf)', line_no=9).assign(target='dbf')
    assets = ln.call(pd.DataFrame(dbf), text='pd.DataFrame(dbf)', line_no=10).assign(target='assets')

    ln.call(
        sns.relplot(
            data=assets,
            x="YEAR_BUILT", y="BLDG_VAL", size='LOT_SIZE'
        ),
        text="""
            sns.relplot(
            data=assets,
            x="YEAR_BUILT", y="BLDG_VAL", size='LOT_SIZE'
        )
        """,
        line_no=11
    )

    """
    Just make sure that it is not ambiguous which of the possibly many functions is running
    assuming there could be name colisions.
    """

    def get_threshold():
        with ln.func(name='get_threshold', ret_text='1970', line_no=12):
            return 1970
    ln.assign(get_threshold, 'get_threshold', 'get_threshold', line_no=21)

    def is_new(col):
        with ln.func(name='is_new', ret_text='col > get_threshold()', line_no=13):
            return col > ln.call(get_threshold(), text='get_threshold()', line_no=14)
    ln.assign(is_new, 'is_new', 'is_new', line_no=22)

    assets['is_new'] = ln.call(is_new(assets['YEAR_BUILT']),
                               text="is_new(assets['YEAR_BUILT'])", line_no=15).assign(target="assets['is_new']")

    clf = ln.call(RandomForestClassifier(random_state=0),
                  text='RandomForestClassifier(random_state=0)',
                  line_no=16
                  ).assign(target='clf')
    # assign(e, target, text, line_no, mod=None):
    y = ln.assign(assets['is_new'], text="assets['is_new']", target='y', line_no=17)
    x = ln.assign(assets[['BLDG_VAL', 'LOT_SIZE', 'NUM_ROOMS']],
                  text="assets[['BLDG_VAL', 'LOT_SIZE', 'NUM_ROOMS']]", line_no=18, target='x')

    ln.call(clf.fit(x, y), text="clf.fit(x, y)", line_no=19)

    p = ln.call(clf.predict([[100 * 1000, 10, 4]]),
                text="clf.predict([[100 * 1000, 10, 4]])",
                line_no=20,
                ).assign(target='p')


