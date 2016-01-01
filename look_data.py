# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 19:58:43 2015

@author: laisijia
"""

import pandas
import matplotlib.pyplot as plt

def mk_time(tb):
    timearr = tb.split("-")
    return (int(timearr[2]) - 10) * 24 + int(timearr[3])

column1 = ['time_bucket', 'id', 'slot', 'click']
column2 = ['time_bucket', 'id', 'slot', 'display']

dtype1 = {'time_bucket':str, 'id':str, 'slot':str, 'click':int}
dtype2 = {'time_bucket':str, 'id':str, 'slot':str, 'display':int}

workdir = "/Users/laisijia/data/ctrpredict/in/"

# load
df1 = pandas.read_csv(workdir + "all_click.tsv", encoding='utf-8', names=column1, dtype=dtype1, sep='\t')
print df1.describe()
print df1.dtypes
df2 = pandas.read_csv(workdir + "all_display.tsv", encoding='utf-8', names=column2, dtype=dtype2, sep='\t')
print df2.describe()
print df2.dtypes

# join
dfctr = pandas.merge(df1, df2, how='right', on=['time_bucket', 'id', 'slot'])
dfctr.fillna(0, inplace=True)

# add column
dfctr['ctr'] = dfctr['click'] * 1.0 / dfctr['display']
dfctr['tb'] = map(mk_time, dfctr['time_bucket'])
print dfctr.describe()

# select
#finaldf = dfctr[['click', 'display', 'ctr']][dfctr['id'] == 201512091422678905]
#201511281557656503 201512091830679813 201512092008680013
finaldf = dfctr[(dfctr['id'] == '201512091422678905') & (dfctr['display']>100) & (dfctr['slot'] == '2-4')]
print finaldf.describe()
print finaldf

finaldf2 = dfctr[(dfctr['id'] == '201512031705666495') & (dfctr['display']>100) & (dfctr['slot'] == '2-4')]
finaldf3 = dfctr[(dfctr['id'] == '201512071047673867') & (dfctr['display']>100) & (dfctr['slot'] == '2-4')]
finaldf4 = dfctr[(dfctr['id'] == '201509121727507235') & (dfctr['display']>100) & (dfctr['slot'] == '2-4')]

fig,ax = plt.subplots(4,2)
ax[0,0].scatter(finaldf['tb'], finaldf['ctr'])
ax[0,1].scatter(finaldf['tb'], finaldf['display'])
ax[1,0].scatter(finaldf2['tb'], finaldf2['ctr'])
ax[1,1].scatter(finaldf2['tb'], finaldf2['display'])
ax[2,0].scatter(finaldf3['tb'], finaldf3['ctr'])
ax[2,1].scatter(finaldf3['tb'], finaldf3['display'])
ax[3,0].scatter(finaldf4['tb'], finaldf4['ctr'])
ax[3,1].scatter(finaldf4['tb'], finaldf4['display'])
#pandas.scatter_matrix(finaldf.ix[0:300])
plt.savefig('foo2.png')
# big ad