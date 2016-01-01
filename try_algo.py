#encoding=utf8

import pandas
import matplotlib.pyplot as plt
import numpy


def get_tb(tb):
    timearr = tb.split('-')
    return 24 * (int(timearr[2]) - 10) + int(timearr[3])

datadir = "/Users/laisijia/data/ctrpredict/in/"

column1 = ['time', 'id', 'slot', 'click']
column2 = ['time', 'id', 'slot', 'display']
dtype1 = {'time':str, 'id':str, 'slot':str, 'click':int}
dtype2 = {'time':str, 'id':str, 'slot':str, 'display':int}

df1 = pandas.read_csv(datadir + "all_click.tsv", encoding='utf8', dtype=dtype1, names=column1, sep='\t')
df2 = pandas.read_csv(datadir + "all_display.tsv", encoding='utf8', dtype=dtype2, names=column2, sep='\t')

# use right join because some data have 0 display but have click
dfctr = pandas.merge(df1, df2, how='right', on=['time','id','slot'])
dfctr.fillna(0)
dfctr['ctr'] = dfctr['click'] * 1.0 / dfctr['display']
dfctr['tb'] = map(get_tb, dfctr['time'])
dfctr['hour'] = map(lambda x: x.split('-')[-1], dfctr['time'])
# print dfctr.describe()

def real(x):
    pos_dict = {'3-3':0.007,
                '1-3':0.015,
                '1-8':0.025,
                '1-23':0.025,
                '2-4':0.014}

    if not numpy.isnan(x[2]):
        return x[2]
    if not numpy.isnan(x[3]):
        return x[3]
    if not numpy.isnan(x[4]):
        return x[4]
    if not numpy.isnan(x[5]):
        return x[5]
    return pos_dict[x[6]]

def feature_extraction(log_time, start_time, day_time, last_hour_time):
    pass

def ctr_agg(src_df, group_arr, display_bar):
    des_df = src_df.groupby(by=group_arr)['click', 'display'].sum().reset_index()
    des_df = des_df[des_df['display'] > display_bar]
    des_df.fillna(0, inplace=True)
    des_df['ctr'] = des_df['click'] / des_df['display']
    return des_df

def print_metrics(log_time, start_time, day_time, last_hour_time):

    df_hour_day = ctr_agg(dfctr[(dfctr['time'] < log_time) & (dfctr['time'] >= day_time) & (dfctr['hour'] == log_time.split('-')[-1])],
                     ['id', 'slot'], 1000)
    df_hours = ctr_agg(dfctr[(dfctr['time'] < log_time) & (dfctr['time'] >= start_time) & (dfctr['hour'] == log_time.split('-')[-1])],
                     ['id', 'slot'], 1000)
    df_last = ctr_agg(dfctr[dfctr['time'] == last_hour_time], ['id', 'slot'], 1000)
    df_day = ctr_agg(dfctr[(dfctr['time'] < log_time) & (dfctr['time'] >= day_time)], ['id', 'slot'], 1000)
    df_7day = ctr_agg(dfctr[(dfctr['time'] < log_time) & (dfctr['time'] >= start_time)], ['id', 'slot'], 1000)
    df_7day_noslot = ctr_agg(dfctr[(dfctr['time'] < log_time) & (dfctr['time'] >= start_time)], ['id'], 1000)

    # test
    dftest = dfctr[dfctr['time'] == log_time].sort_values(by=['id','slot'])

    testh1 = pandas.merge(df_hour_day, dftest, how='right', on=['id','slot'], sort=True)
    testh = pandas.merge(df_hours, dftest, how='right', on=['id','slot'], sort=True)
    testlast = pandas.merge(df_last, dftest, how='right', on=['id','slot'], sort=True)
    test1 = pandas.merge(df_day, dftest, how='right', on=['id','slot'], sort=True)
    baselinetest = pandas.merge(df_7day, dftest, how='right', on=['id','slot'], sort=True)
    baselinefinal = pandas.merge(df_7day_noslot, dftest, how='right', on=['id'], sort=True)

    baselinetest['pctr'] = map(real, zip(testh1['ctr_x'], testh['ctr_x'], testlast['ctr_x'], test1['ctr_x'], baselinetest['ctr_x'], baselinefinal['ctr_x'], dftest['slot']))
    baselinetest.fillna(0, inplace=True)
    baselinetest['click_bias'] = map(lambda x: abs(x), (baselinetest['pctr']*baselinetest['display_y']) - baselinetest['click_y'])
    # bad case study
    # print baselinetest.sort(['click_bias'], ascending=[0]).reset_index().ix[0:3]
    click = baselinetest['click_y'].sum()
    display = baselinetest['display_y'].sum()
    ctr = click / display
    pclick = baselinetest['pctr'].dot(baselinetest['display_y'])
    pctr = baselinetest['pctr'].dot(baselinetest['display_y']) / baselinetest['display_y'].sum()
    clickbias = baselinetest['click_bias'].sum()
    deltaclick = clickbias / click
    #sqclick = reduce(lambda x,y:x+y, map(lambda x: x**2, (baselinetest['pctr']*baselinetest['display_y']) - baselinetest['click_y'])) / (click * click)
    print "\t".join(map(lambda x:str(x), [log_time, start_time, display, click, ctr, pctr, pclick, deltaclick, clickbias]))

for log_date in range(17, 22, 1):
    for log_hour in xrange(0, 24):
        log_hour_str = str(log_hour) if log_hour >= 10 else "0" + str(log_hour)
        last_hour_str = str(log_hour - 1) if log_hour >= 11 else "0" + str(log_hour - 1)
        log_str = "2015-12-" + str(log_date) + "-" + log_hour_str
        start_str = '2015-12-' + str(log_date - 7) + '-00'
        day_str = '2015-12-' + str(log_date - 1) + '-00'
        if log_hour == 0:
            hour_str = '2015-12-' + str(log_date - 1) + '-23'
        else:
            hour_str = "2015-12-" + str(log_date) + "-" + last_hour_str

        print_metrics(log_str, start_str, day_str, hour_str)