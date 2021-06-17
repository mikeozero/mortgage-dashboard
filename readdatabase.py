import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# conn = db.create_engine('postgresql+psycopg2://postgres:88888888@localhost:5432/mortgage',{})
conn = db.create_engine('mysql+pymysql://root:root@localhost:3306/mortgage',{})
df = pd.read_sql('select * from VW_RESD_MTGE_OA_RISK',con=conn)

sort_list = ['Q4-13','Q1-14','Q2-14','Q3-14','Q4-14']

base = df.loc[:,['QUARTER_YEAR','REGION','DAY_PST_DUE']]
da = base['DAY_PST_DUE'].map(lambda x: 1 if x else 0)
base['DEL_ACCT'] = da

### df for reportable delinquency rate
de = base.groupby(['QUARTER_YEAR']).agg(total=('DAY_PST_DUE','size'))
rpt = base[base['DAY_PST_DUE']>30].groupby(['QUARTER_YEAR']).agg(total=('DAY_PST_DUE','size'))
gt90 = base[base['DAY_PST_DUE']>90].groupby(['QUARTER_YEAR']).agg(total=('DAY_PST_DUE','size'))
gt30 = base[(base['DAY_PST_DUE']>30)&(base['DAY_PST_DUE']<=90)].groupby(['QUARTER_YEAR']).agg(total=('DAY_PST_DUE','size'))
de['rpt']=rpt['total']
de['gt30']=gt30['total']
de['gt90']=gt90['total']
de['rpt_rate']=round(de['rpt']*100/de['total'],2)
de['gt30_rate']=round(de['gt30']*100/de['total'],2)
de['gt90_rate']=round(de['gt90']*100/de['total'],2)
de = de.loc[sort_list]
de = de[['gt90_rate','gt30_rate','rpt_rate']]
de


### df for regional delinquency account:
# all canada:
ac = base.groupby(['QUARTER_YEAR']).agg(total=('DEL_ACCT','size'),deac=('DEL_ACCT','sum'))
ac['del_rate']=round(ac['deac']*100/ac['total'],2)
ac = ac.loc[:,['del_rate']]
ac = ac.loc[sort_list]

rde = base.groupby(['REGION','QUARTER_YEAR']).agg(total=('DEL_ACCT','size'),deac=('DEL_ACCT','sum'))

# add toronto to ontario
qt = rde.index.get_level_values(1).unique()
for i in qt:
    rde.loc['Ontario'].loc[i,'total'] += rde.loc['Toronto'].loc[i,'total']
    rde.loc['Ontario'].loc[i,'deac'] += rde.loc['Toronto'].loc[i,'deac']

rde['del_rate']=round(rde['deac']*100/rde['total'],2)

rde = rde.loc[:,['del_rate']].unstack(level=0)
rde = rde.loc[sort_list]['del_rate']
rde['All Canada'] = ac['del_rate']
rde = rde[['Atlantic','BC','Ontario','Prairies','Quebec','Toronto','All Canada']]
rde


### df for LTV
data = df[df['DEFLT_INSUR_CD'].map(lambda x:True if x.lower()=='uninsured' else False)].loc[:,['QUARTER_YEAR','CRNT_LTV_RATIO','OS_BAL_AMT','CRNT_PRPTY_VAL_AMT']]

# quarter avg ltv
avg = data.groupby(['QUARTER_YEAR']).agg(totalbal=('OS_BAL_AMT','sum'),totalval=('CRNT_PRPTY_VAL_AMT','sum'))
avg['avg_ltv'] = round(avg['totalbal']*100/avg['totalval'],2)
avg = avg.loc[:,['avg_ltv']]
avg = avg.loc[sort_list]

ltv = data.groupby(['QUARTER_YEAR']).agg(total=('CRNT_LTV_RATIO','size'))
lt50 = data[data['CRNT_LTV_RATIO']<=0.5].groupby(['QUARTER_YEAR']).agg(total=('CRNT_LTV_RATIO','size'))
bt5060 = data[(data['CRNT_LTV_RATIO']>0.5)&(data['CRNT_LTV_RATIO']<=0.6)].groupby(['QUARTER_YEAR']).agg(total=('CRNT_LTV_RATIO','size'))
bt6070 = data[(data['CRNT_LTV_RATIO']>0.6)&(data['CRNT_LTV_RATIO']<=0.7)].groupby(['QUARTER_YEAR']).agg(total=('CRNT_LTV_RATIO','size'))
bt7080 = data[(data['CRNT_LTV_RATIO']>0.7)&(data['CRNT_LTV_RATIO']<=0.8)].groupby(['QUARTER_YEAR']).agg(total=('CRNT_LTV_RATIO','size'))
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
ltv['avg'] = avg['avg_ltv']
ltv = ltv[['l5rt','b56rt','b67rt','b78rt','avg']]
ltv