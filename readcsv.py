import pandas as pd

df = pd.read_csv('sources/mortgage.csv')

sort_list = ['Q4-13','Q1-14','Q2-14','Q3-14','Q4-14']

# Add Quarter-Year column:
def countQuarters(x):
    if x:
        qt = int(x.strip()[5:7])
        y = x.strip()[2:4]
        if qt == 1:
            return 'Q1-'+y
        elif qt in (2,3,4):
            return 'Q2-'+y
        elif qt in (5,6,7):
            return 'Q3-'+y
        elif qt in (8,9,10):
            return 'Q4-'+y
        elif qt in (11,12):
            return 'Q1-'+str(int(y)+1)
    else:
        return None
qy = df['date'].map(lambda x:countQuarters(x))
df['quarter_year']=qy

### reportable delinquency:
base = df.loc[:,['quarter_year','del_days']]
de = base.groupby(['quarter_year']).agg(total=('del_days','size'))
reportable = base[base['del_days']>30].groupby(['quarter_year']).agg(total=('del_days','size'))
gt90 = base[base['del_days']>90].groupby(['quarter_year']).agg(total=('del_days','size'))
gt30 = base[(base['del_days']>30)&(base['del_days']<=90)].groupby(['quarter_year']).agg(total=('del_days','size'))
de['reportable']=reportable['total']
de['gt30']=gt30['total']
de['gt90']=gt90['total']
de['rpt_rate']=round(de['reportable']*100/de['total'],2)
de['gt30_rate']=round(de['gt30']*100/de['total'],2)
de['gt90_rate']=round(de['gt90']*100/de['total'],2)
de = de.loc[sort_list]
de = de[['gt90_rate','gt30_rate','rpt_rate']]
de   # fianl reportable delinquency rate df


# LTV of new uninsured mortgages:
data = df[df['insur_type']=='uninsured']
data = data.loc[:,['ltv','quarter_year','balance']]
data['prop_val'] = round(data['balance']/data['ltv'],0)
avg = data.groupby(['quarter_year']).agg(totalbal=('balance','sum'),totalval=('prop_val','sum'))
avg['avg_ltv'] = round(avg['totalbal']*100/avg['totalval'],2)
avg = avg.loc[:,['avg_ltv']]
avg = avg.loc[sort_list]
ltv = data.groupby(['quarter_year']).agg(total=('ltv','size'))
lt50 = data[data['ltv']<=0.5].groupby(['quarter_year']).agg(total=('ltv','size'))
bt5060 = data[(data['ltv']>0.5)&(data['ltv']<=0.6)].groupby(['quarter_year']).agg(total=('ltv','size'))
bt6070 = data[(data['ltv']>0.6)&(data['ltv']<=0.7)].groupby(['quarter_year']).agg(total=('ltv','size'))
bt7080 = data[(data['ltv']>0.7)&(data['ltv']<=0.8)].groupby(['quarter_year']).agg(total=('ltv','size'))
ltv['lt50'] = lt50['total']
ltv['bt5060'] = bt5060['total']
ltv['bt6070'] = bt6070['total']
ltv['bt7080'] = bt7080['total']
ltv = ltv.where(ltv.notnull(),0)
ltv['l5rt'] = round(ltv['lt50']*100/ltv['total'],2)
ltv['b56rt'] = round(ltv['bt5060']*100/ltv['total'],2)
ltv['b67rt'] = round(ltv['bt6070']*100/ltv['total'],2)
ltv['b78rt'] = round(ltv['bt7080']*100/ltv['total'],2)
ltv = ltv.loc[sort_list]
ltv = ltv[['l5rt','b56rt','b67rt','b78rt']]
ltv['avg'] = avg['avg_ltv']
ltv   # ltv rate df, maynot by corract, no avg ltv data...need to be added


# Add Region column:
def countRegion(x):
    if x:
        code = x.strip()[0].upper()
        if code in ('T','S','R'):
            return 'Prairies'
        elif code in ('A','B','C','E'):
            return 'Atlantic'
        elif code in ('V'):
            return 'BC'
        elif code in ('H','G','J'):
            return 'Quebec'
        elif code in ('P','L','N','K'):
            return 'Ontario'
        elif code in ('M'):
            return 'Toronto'
        else:
            return 'Other'
    else:
        return 'Ontario'
region = df['postal'].map(lambda x:countRegion(x))
df['region']=region

### delinquency account:
da = df['del_days'].map(lambda x: 1 if x else 0)
df['delinquency_account']=da
qr=df.loc[:,['delinquency_account','quarter_year','region']]

# all canada:
ac = qr.groupby(['quarter_year']).agg(total=('delinquency_account','size'),deac=('delinquency_account','sum'))
ac['del_rate']=round(ac['deac']*100/ac['total'],2)
ac = ac.loc[:,['del_rate']]
ac = ac.loc[sort_list]


rde = qr.groupby(['region','quarter_year']).agg(total=('delinquency_account','size'),deac=('delinquency_account','sum'))

# add toronto to ontario
qlist = rde.index.get_level_values(1).unique()
for i in qlist:
    rde.loc['Ontario'].loc[i,'total'] += rde.loc['Toronto'].loc[i,'total']
    rde.loc['Ontario'].loc[i,'deac'] += rde.loc['Toronto'].loc[i,'deac']

rde['del_rate']=round(rde['deac']*100/rde['total'],2)

rde = rde.loc[:,['del_rate']].unstack(level=0)
rde = rde.loc[sort_list]['del_rate']
rde['All Canada'] = ac['del_rate']
rde = rde[['Atlantic','BC','Ontario','Prairies','Quebec','Toronto','All Canada']]
rde  # final regional delinquency rate df

