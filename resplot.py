import pandas
import numpy
import matplotlib.pyplot as plt

names = ['log_time', 'start_time', 'display', 'click', 'ctr', 'pctr', 'pclick', 'deltaclick', 'sqclick']
names2 = ['log_time', 'start_time', 'display', 'click', 'ctr', 'pctr', 'pclick', 'deltaclick', 'sqclick', 'click_bias']
df1 = pandas.read_csv("1.tsv", encoding='utf8', names=names2, sep='\t')
df2 = pandas.read_csv("2.tsv", encoding='utf8', names=names, sep='\t')
df3 = pandas.read_csv("3.tsv", encoding='utf8', names=names, sep='\t')
df4 = pandas.read_csv("4.tsv", encoding='utf8', names=names, sep='\t')
df5 = pandas.read_csv("5.tsv", encoding='utf8', names=names, sep='\t')
df6 = pandas.read_csv("6.tsv", encoding='utf8', names=names, sep='\t')
df7 = pandas.read_csv("7.tsv", encoding='utf8', names=names, sep='\t')
df8 = pandas.read_csv("8.tsv", encoding='utf8', names=names, sep='\t')
df9 = pandas.read_csv("9.tsv", encoding='utf8', names=names, sep='\t')
df10 = pandas.read_csv("10.tsv", encoding='utf8', names=names, sep='\t')
df11 = pandas.read_csv("11.tsv", encoding='utf8', names=names, sep='\t')
df12 = pandas.read_csv("12.tsv", encoding='utf8', names=names, sep='\t')
df13 = pandas.read_csv("13.tsv", encoding='utf8', names=names, sep='\t')
df14 = pandas.read_csv("14.tsv", encoding='utf8', names=names, sep='\t')
df15 = pandas.read_csv("15.tsv", encoding='utf8', names=names, sep='\t')
df16 = pandas.read_csv("16.tsv", encoding='utf8', names=names, sep='\t')
df17 = pandas.read_csv("17.tsv", encoding='utf8', names=names, sep='\t')
df18 = pandas.read_csv("18.tsv", encoding='utf8', names=names2, sep='\t')
df19 = pandas.read_csv("19.tsv", encoding='utf8', names=names2, sep='\t')

plt.plot(df1['click'])
plt.plot(df1['deltaclick'] * df1['click'])
plt.plot(df2['deltaclick'] * df2['click'])
plt.plot(df3['deltaclick'] * df3['click'])
#plt.plot(df4['deltaclick'])
#plt.plot(df5['deltaclick'])
plt.plot(df6['deltaclick'] * df6['click'])
#plt.plot(df7['deltaclick'])
#plt.plot(df8['deltaclick'])
#plt.plot(df9['deltaclick'])
#plt.plot(df10['deltaclick'])
#plt.plot(df11['deltaclick'])
#plt.plot(df12['deltaclick'])
#plt.plot(df13['deltaclick'])
#plt.plot(df14['deltaclick'])
#plt.plot(df15['deltaclick'])
#plt.plot(df16['deltaclick'])
#plt.plot(df17['deltaclick'])
plt.plot(df18['deltaclick'] * df18['click'])
#plt.plot(df19['sqclick'])
#plt.plot(df18['deltaclick'] - df1['deltaclick'])

plt.legend([
#    'prod',
#    '0.015',
#    'slot', # only slot, similiar with prod
#    'no slot', #only noslot, similiar with prod
#    '3 days', # 3 days time window, similiar with prod, slightly better
#    'hour', # 7 days same hour data, worse than prod
#    'hour with 50bar', # similiar with 'hour',
#    '200bar',
#    'defaultslot', # change 0.015 to slot overall ctr, similiar with prod
#    'onlyslot', # similiar with 0.015, better
#    'defaultslot10000', # prod, worse
#    'defaultslotnoslot10000', # prod, worse
#    'defaultslotnoslot100', # prod, same
#    '1 day', #prod slightly better
#    '1 day 100', #prod better
#    'histogram', #same quality but diff graph, not good
#    'histogram without hour', # not obvious, try bad case study
#    'circle10000',
#    'circle1000'
    '0', '1', '2', '3','6', '18'
], loc='upper left')
plt.savefig('foo.png')