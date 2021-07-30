import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# conn = db.create_engine('postgresql+psycopg2://postgres:88888888@localhost:5432/mortgage',{})
conn = db.create_engine('mysql+pymysql://root:root@localhost:3306/mortgage',{})
df = pd.read_sql('select * from VW_RESD_MTGE_OA_RISK',con=conn)  # mortgage
dfcc = pd.read_sql('select * from VW_CREDIT_CARD_RISK',con=conn)  # credit card

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
data = df[df['DEFLT_INSUR_CD'].map(lambda x:True if x.lower()=='uninsured' else False)].loc[:,['QUARTER_YEAR','CRNT_LTV_RATIO','OS_BAL_AMT','CRNT_PRPTY_VAL_AMT','TM_ON_BOOK']]
data = data[data['TM_ON_BOOK']==1]
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

# new uninsured auth limit distribution by amortization range:
dfar = df[(df['DEFLT_INSUR_CD'].map(lambda x:True if x.lower()=='uninsured' else False))&(df['TM_ON_BOOK']==1)].loc[:,['QUARTER_YEAR','CRNT_AUTH_LIMIT_AMT','RMNG_AMORT_PERIOD','TM_ON_BOOK']]
amr = dfar.groupby('QUARTER_YEAR').agg(total=('CRNT_AUTH_LIMIT_AMT','sum'))
amrlt20 = dfar[dfar['RMNG_AMORT_PERIOD']<=20].groupby('QUARTER_YEAR').agg(total=('CRNT_AUTH_LIMIT_AMT','sum'))
amrlt25 = dfar[(dfar['RMNG_AMORT_PERIOD']>20)&(dfar['RMNG_AMORT_PERIOD']<=25)].groupby('QUARTER_YEAR').agg(total=('CRNT_AUTH_LIMIT_AMT','sum'))
amrgt25 = dfar[dfar['RMNG_AMORT_PERIOD']>25].groupby('QUARTER_YEAR').agg(total=('CRNT_AUTH_LIMIT_AMT','sum'))
amr['lt20'] = amrlt20['total']
amr['lt25'] = amrlt25['total']
amr['gt25'] = amrgt25['total']
amr['lt20rt'] = round(amr['lt20']*100/amr['total'],0)
amr['lt25rt'] = round(amr['lt25']*100/amr['total'],0)
amr['gt25rt'] = round(amr['gt25']*100/amr['total'],0)
amr = amr[['lt20rt','lt25rt','gt25rt']].loc[sort_list]
amr


### credit card: ###
basecc = dfcc.loc[:,['QUARTER_YEAR','REGION','DAY_PST_DUE','CRNT_AUTH_LIMIT_AMT','PRD_TYPE','CREDIT_RISK_INDICATOR','OS_BAL_AMT','TM_ON_BOOK']]
dacc = basecc['DAY_PST_DUE'].map(lambda x: 1 if x else 0)
basecc['DEL_ACCT'] = dacc
# credit card delinquency
decc = basecc.groupby(['QUARTER_YEAR']).agg(total=('DAY_PST_DUE','size'))
rptcc = basecc[basecc['DAY_PST_DUE']>30].groupby(['QUARTER_YEAR']).agg(total=('DAY_PST_DUE','size'))
gt90cc = basecc[basecc['DAY_PST_DUE']>90].groupby(['QUARTER_YEAR']).agg(total=('DAY_PST_DUE','size'))
gt30cc = basecc[(basecc['DAY_PST_DUE']>30)&(basecc['DAY_PST_DUE']<=90)].groupby(['QUARTER_YEAR']).agg(total=('DAY_PST_DUE','size'))
decc['rpt']=rptcc['total']
decc['gt30']=gt30cc['total']
decc['gt90']=gt90cc['total']
decc['rpt_rate']=round(decc['rpt']*100/decc['total'],2)
decc['gt30_rate']=round(decc['gt30']*100/decc['total'],2)
decc['gt90_rate']=round(decc['gt90']*100/decc['total'],2)
decc = decc.loc[sort_list]
decc = decc[['gt90_rate','gt30_rate','rpt_rate']]
decc

# credit card regional delinquency:
# all canada:
acc = basecc.groupby(['QUARTER_YEAR']).agg(total=('DEL_ACCT','size'),deac=('DEL_ACCT','sum'))
acc['del_rate']=round(acc['deac']*100/acc['total'],2)
acc = acc.loc[:,['del_rate']]
acc = acc.loc[sort_list]
rdecc = basecc.groupby(['REGION','QUARTER_YEAR']).agg(total=('DEL_ACCT','size'),deac=('DEL_ACCT','sum'))
# add toronto to ontario
qtcc = rdecc.index.get_level_values(1).unique()
for i in qtcc:
    rdecc.loc['Ontario'].loc[i,'total'] += rdecc.loc['Toronto'].loc[i,'total']
    rdecc.loc['Ontario'].loc[i,'deac'] += rdecc.loc['Toronto'].loc[i,'deac']
rdecc['del_rate']=round(rdecc['deac']*100/rdecc['total'],2)
rdecc = rdecc.loc[:,['del_rate']].unstack(level=0)
rdecc = rdecc.loc[sort_list]['del_rate']
rdecc['All Canada'] = acc['del_rate']
rdecc = rdecc[['Atlantic','BC','Ontario','Prairies','Quebec','Toronto','All Canada']]
rdecc

# visa and amex total limit
lmt = basecc[((basecc['PRD_TYPE']=='AMEX')|(basecc['PRD_TYPE']=='VISA'))&(basecc['TM_ON_BOOK']==1)]
lmt = lmt.groupby(['PRD_TYPE','QUARTER_YEAR']).agg(total=('CRNT_AUTH_LIMIT_AMT','sum'))
lmt = lmt.unstack(0)['total'].loc[sort_list]
lmt = round(lmt/1000000,2)
lmt

# %outstandings by cri
cricc = basecc['CREDIT_RISK_INDICATOR'].map(lambda x: 'A+B' if x in ('a','b') else 'C' if x=='c' else 'D+E')
basecc['CRI'] = cricc
cri = basecc.groupby(['QUARTER_YEAR']).agg(total=('OS_BAL_AMT','sum'))
criab = basecc[basecc['CRI']=='A+B'].groupby(['QUARTER_YEAR']).agg(total=('OS_BAL_AMT','sum'))
cric = basecc[basecc['CRI']=='C'].groupby(['QUARTER_YEAR']).agg(total=('OS_BAL_AMT','sum'))
cride = basecc[basecc['CRI']=='D+E'].groupby(['QUARTER_YEAR']).agg(total=('OS_BAL_AMT','sum'))
cri['AB'] = criab['total']
cri['C'] = cric['total']
cri['DE'] = cride['total']
cri = cri.where(cri.notnull(),0)
cri['abrt'] = round(cri['AB']*100/cri['total'],2)
cri['crt'] = round(cri['C']*100/cri['total'],2)
cri['dert'] = round(cri['DE']*100/cri['total'],2)
cri = cri[['abrt','crt','dert']].loc[sort_list]
cri