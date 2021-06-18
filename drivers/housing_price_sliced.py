import gadget as ln
with ln.tracking('housing_price'):

    import dbfread
    import pandas as pd

    from sklearn.ensemble import RandomForestClassifier


    ln.importing(dbfread, module='dbfread', name='dbfread', line_no=2) ###############################
    ln.importing(pd, module='pandas', name='pd', line_no=3) ##########################################

    ln.importing(RandomForestClassifier, module='sklearn.ensemble.RandomForestClassifier', name='RandomForestClassifier', line_no=5) ##############################


    dbf = ln.call(dbfread.DBF("../property_example/L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf"),
                  text='dbfread.DBF("./L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf")', line_no=8,
                  args=[('./L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf', "'./L3_SHP_M114_Greenfield/M114Assess_CY20_FY20.dbf'"),]
                  ).assign(target='dbf') ################################################################################################################
    dbf = ln.call(iter(dbf), text='iter(dbf)', line_no=9, args=[(dbf, 'dbf')]).assign(target='dbf') #####################################################
    assets = ln.call(pd.DataFrame(dbf), text='pd.DataFrame(dbf)', line_no=10, args=[(dbf, 'dbf')]).assign(target='assets') ##############################


    """
    Just make sure that it is not ambiguous which of the possibly many functions is running
    assuming there could be name colisions.
    """

    def get_threshold(): ###############################################################################################
        with ln.func(name='get_threshold', args=None, ret_text='1970', line_no=12):
            return 1970
    ln.assign(get_threshold, 'get_threshold', 'get_threshold', line_no=21)

    def is_new(col): ###################################################################################################
        with ln.func(name='is_new', args=[(col, 'col'),], ret_text='col > get_threshold()', line_no=13):
            return col > ln.call(get_threshold(), text='get_threshold()', line_no=14)
    ln.assign(is_new, 'is_new', 'is_new', line_no=22)

    assets['is_new'] = ln.call(is_new(assets['YEAR_BUILT']),
                               text="is_new(assets['YEAR_BUILT'])", line_no=15, args=[(assets['YEAR_BUILT'],
                                                                                       "assets['YEAR_BUILT']")]
                               ).assign(target="assets") ###############################################################

    clf = ln.call(RandomForestClassifier(random_state=0),
                  text='RandomForestClassifier(random_state=0)',
                  line_no=16,
                  args=[(0, {'random_state': '0'}), ]
                  ).assign(target='clf') ###############################################################################
    # assign(e, target, text, line_no, mod=None):
    y = ln.assign(assets['is_new'], text="assets", target='y', line_no=17) #############################################
    x = ln.assign(assets[['BLDG_VAL', 'LOT_SIZE', 'NUM_ROOMS']],
                  text="assets", line_no=18, target='x')                   #############################################

    ln.call(clf.fit(x, y), text="clf.fit(x, y)", line_no=19, args=[(x, 'x'), (y, 'y')]) ################################

    p = ln.call(clf.predict([[100 * 1000, 10, 4]]),
                text="clf.predict([[100 * 1000, 10, 4]])",
                line_no=20,
                args=[([[100 * 1000, 10, 4]], "[[100 * 1000, 10, 4]]")]
                ).assign(target='p') ###################################################################################

    # import sqlite3
    # ln.importing(sqlite3, module='sqlite3', name='sqlite3', line_no=21)
    #
    #
    # con = ln.call(sqlite3.connect('demo.db'), text="sqlite3.connect('demo.db')", line_no=22, args=[('demo.db',
    #                                                                                                 "'demo.db'")]
    #               ).assign(target='con')
    # ln.call(pd.read_sql('SELECT * FROM data_assets', con),
    #         text="pd.read_sql('SELECT * FROM data_assets', con)",
    #         line_no=23,
    #         args=[('SELECT * FROM data_assets', "'SELECT * FROM data_assets'"),
    #               (con, 'con')])
