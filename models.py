from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from datetime import datetime,timedelta

# change file paths:
prdPath = 'sources/Data_Product Hierarchy.xlsx'
acctPath = 'sources/mortgage.csv'
creditPath = 'sources/credit_card.csv'

app = Flask(__name__)

# change database uri:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:88888888@localhost:5432/mortgage'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/mortgage?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxxxxxxxx'

db = SQLAlchemy(app)

dfp = pd.read_excel(prdPath,sheet_name=0,engine='openpyxl')
dfp = dfp.where(dfp.notnull(),None)
dfa = pd.read_csv(acctPath)
dfa = dfa.where(dfa.notnull(),None)
dfc = pd.read_csv(creditPath)
dfc = dfc.where(dfc.notnull(),None)

class DATA_PRODUCT_MAPPING_LKP(db.Model):
    __tablename__ = 'DATA_PRODUCT_MAPPING_LKP'
    PRD_CD = db.Column(db.Integer, primary_key=True)
    IB_CB_INDICATOR = db.Column(db.String(2), nullable=False)
    PRD_LVL1 = db.Column(db.String(50))
    PRD_LVL2 = db.Column(db.String(50))
    PRD_LVL3 = db.Column(db.String(50))
    PRD_LVL4 = db.Column(db.String(50))
    PRD_LVL5 = db.Column(db.String(50))
    EFF_FROM_DT = db.Column(db.Date)
    EFF_TO_DT = db.Column(db.Date)
    CRNT_F = db.Column(db.String(1))
    INSRT_PROCESS_TMSTMP = db.Column(db.DECIMAL)
    UPDT_PROCESS_TMSTMP = db.Column(db.DECIMAL)

class Acct_perf(db.Model):
    __tablename__ = 'Acct_perf'
    ACCT_NUM = db.Column(db.Integer,primary_key=True)
    PRD_CD = db.Column(db.Integer,db.ForeignKey('DATA_PRODUCT_MAPPING_LKP.PRD_CD'))
    CREDIT_RISK_INDICATOR = db.Column(db.String(20))
    TM_ON_BOOK = db.Column(db.Integer)
    DAY_PST_DUE = db.Column(db.Integer)
    RMNG_AMORT_PERIOD = db.Column(db.Integer)
    DEFLT_INSUR_CD = db.Column(db.String(20))
    CRNT_AUTH_LIMIT_AMT = db.Column(db.DECIMAL)
    OS_BAL_AMT = db.Column(db.DECIMAL)
    PRPTY_TYPE_CD = db.Column(db.String(20))
    PRPTY_POSTAL_CD = db.Column(db.String(6))
    CRNT_LTV_RATIO = db.Column(db.Float)
    MTH_END_DT = db.Column(db.Date)
    INSURANCE_FEE_INDICATOR = db.Column(db.String(5))

    PROD = db.relationship('DATA_PRODUCT_MAPPING_LKP', backref='ACCS')

class Acct_Credit(db.Model):
    __tablename__ = 'Acct_Credit'
    ACCT_NUM = db.Column(db.Integer,primary_key=True)
    PRD_CD = db.Column(db.Integer,db.ForeignKey('DATA_PRODUCT_MAPPING_LKP.PRD_CD'))
    MTH_END_DT = db.Column(db.Date)
    CREDIT_RISK_INDICATOR = db.Column(db.String(20))
    DAY_PST_DUE = db.Column(db.Integer)
    POSTAL_CD = db.Column(db.String(6))
    OS_BAL_AMT = db.Column(db.DECIMAL)
    PREMIUM = db.Column(db.String(5))
    CRNT_AUTH_LIMIT_AMT = db.Column(db.DECIMAL)
    TM_ON_BOOK = db.Column(db.Integer)

    PROD = db.relationship('DATA_PRODUCT_MAPPING_LKP', backref='CCS')


# add new product or update changed product
def updtprd(row):
    if row['Product Code']:
        record = DATA_PRODUCT_MAPPING_LKP.query.filter_by(PRD_CD=row['Product Code']).first()
        if not record:
            prd = DATA_PRODUCT_MAPPING_LKP(
                PRD_CD=row['Product Code'],
                IB_CB_INDICATOR=row['IB CB Indicator'],
                PRD_LVL1=row['Product Hierarchy Level 1 Description'],
                PRD_LVL2=row['Product Hierarchy Level 2 Description'],
                PRD_LVL3=row['Product Hierarchy Level 3 Description'],
                PRD_LVL4=row['Product Hierarchy Level 4 Description'],
                PRD_LVL5=row['Product Hierarchy Level 5'],
                EFF_FROM_DT='2000-01-01',
                EFF_TO_DT='9999-12-31',
                CRNT_F='Y',
                INSRT_PROCESS_TMSTMP=datetime.timestamp(datetime.now())
            )
            db.session.add(prd)
            db.session.commit()
        else:
            if row['IB CB Indicator'] != record.IB_CB_INDICATOR or row['Product Hierarchy Level 1 Description'] != record.PRD_LVL1 or row['Product Hierarchy Level 2 Description'] != record.PRD_LVL2 or row['Product Hierarchy Level 3 Description'] != record.PRD_LVL3 or row['Product Hierarchy Level 4 Description'] != record.PRD_LVL4 or row['Product Hierarchy Level 5'] != record.PRD_LVL5:
                print('---------updating prdcd: {} ---------'.format(row['Product Code']))
                record.IB_CB_INDICATOR = row['IB CB Indicator']
                record.PRD_LVL1 = row['Product Hierarchy Level 1 Description']
                record.PRD_LVL2 = row['Product Hierarchy Level 2 Description']
                record.PRD_LVL3 = row['Product Hierarchy Level 3 Description']
                record.PRD_LVL4 = row['Product Hierarchy Level 4 Description']
                record.PRD_LVL5 = row['Product Hierarchy Level 5']
                record.UPDT_PROCESS_TMSTMP = datetime.timestamp(datetime.now())
                db.session.commit()

# add new acct or update changed acct
def updtacct(row):
    if row['acct_num']:
        record = Acct_perf.query.filter_by(ACCT_NUM=row['acct_num']).first()
        if not record:
            acct = Acct_perf(
                ACCT_NUM=row['acct_num'],
                PRD_CD=row['product_code'],
                CREDIT_RISK_INDICATOR=row['cc_cri'],
                TM_ON_BOOK=row['tm_on_book_month'],
                DAY_PST_DUE=row['del_days'],
                RMNG_AMORT_PERIOD=row['amortization_years'],
                DEFLT_INSUR_CD=row['insur_type'],
                CRNT_AUTH_LIMIT_AMT=row['auth_limit'],
                OS_BAL_AMT=row['balance'],
                PRPTY_TYPE_CD='condo' if row['condo'].lower()=='yes' else None,
                PRPTY_POSTAL_CD=row['postal'],
                CRNT_LTV_RATIO=row['ltv'],
                MTH_END_DT=row['date'],
                INSURANCE_FEE_INDICATOR=row['premium']
            )
            db.session.add(acct)
            db.session.commit()
        else:
            if row['product_code'] != record.PRD_CD or row['cc_cri'] != record.CREDIT_RISK_INDICATOR or row['tm_on_book_month'] != record.TM_ON_BOOK or row['del_days'] != record.DAY_PST_DUE \
                    or row['amortization_years'] != record.RMNG_AMORT_PERIOD or row['insur_type'] != record.DEFLT_INSUR_CD or row['auth_limit'] != record.CRNT_AUTH_LIMIT_AMT \
                    or row['balance'] != record.OS_BAL_AMT or row['condo'].lower() != ('yes' if record.PRPTY_TYPE_CD=='condo' else 'no') or row['postal'] != record.PRPTY_POSTAL_CD \
                    or row['ltv'] != record.CRNT_LTV_RATIO or row['date'] != record.MTH_END_DT.strftime('%Y-%m-%d') or row['premium'] != record.INSURANCE_FEE_INDICATOR:
                print('---------update acctnum: {} ---------'.format(row['acct_num']))
                record.PRD_CD = row['product_code']
                record.CREDIT_RISK_INDICATOR = row['cc_cri']
                record.TM_ON_BOOK = row['tm_on_book_month']
                record.DAY_PST_DUE = row['del_days']
                record.RMNG_AMORT_PERIOD = row['amortization_years']
                record.DEFLT_INSUR_CD = row['insur_type']
                record.CRNT_AUTH_LIMIT_AMT = row['auth_limit']
                record.OS_BAL_AMT = row['balance']
                record.PRPTY_TYPE_CD = 'condo' if row['condo'].lower()=='yes' else None
                record.PRPTY_POSTAL_CD = row['postal']
                record.CRNT_LTV_RATIO = row['ltv']
                record.MTH_END_DT = row['date']
                record.INSURANCE_FEE_INDICATOR = row['premium']
                db.session.commit()

# add new credit card record or update changed record
def updtcredit(row):
    if row['acct_num']:
        record = Acct_Credit.query.filter_by(ACCT_NUM=row['acct_num']).first()
        if not record:
            acct = Acct_Credit(
                ACCT_NUM=row['acct_num'],
                PRD_CD=row['product_code'],
                MTH_END_DT=row['date'],
                CREDIT_RISK_INDICATOR=row['cc_cri'],
                DAY_PST_DUE=row['del_days'],
                POSTAL_CD=row['postal'],
                OS_BAL_AMT=row['balance'],
                PREMIUM=row['premium'],
                CRNT_AUTH_LIMIT_AMT=row['auth_limit'],
                TM_ON_BOOK=row['tm_on_book_month']
            )
            db.session.add(acct)
            db.session.commit()
        else:
            if row['product_code'] != record.PRD_CD or row['cc_cri'] != record.CREDIT_RISK_INDICATOR or row['tm_on_book_month'] != record.TM_ON_BOOK \
                    or row['del_days'] != record.DAY_PST_DUE or row['auth_limit'] != record.CRNT_AUTH_LIMIT_AMT \
                    or row['balance'] != record.OS_BAL_AMT or row['postal'] != record.POSTAL_CD \
                    or row['date'] != record.MTH_END_DT.strftime('%Y-%m-%d') or row['premium'] != record.PREMIUM:
                print('---------update acctnum: {} ---------'.format(row['acct_num']))
                record.PRD_CD = row['product_code']
                record.CREDIT_RISK_INDICATOR = row['cc_cri']
                record.TM_ON_BOOK = row['tm_on_book_month']
                record.DAY_PST_DUE = row['del_days']
                record.CRNT_AUTH_LIMIT_AMT = row['auth_limit']
                record.OS_BAL_AMT = row['balance']
                record.POSTAL_CD = row['postal']
                record.MTH_END_DT = row['date']
                record.PREMIUM = row['premium']
                db.session.commit()

def readProduct(df):
    df.apply(updtprd,axis=1)
    print('------------------finished update products table-----------------')

def readCSV(df):
    df.apply(updtacct,axis=1)
    print('------------------finished update acct perf table-----------------')

def readCredit(df):
    df.apply(updtcredit,axis=1)
    print('------------------finished update acct credit table-----------------')

# inactive prd that not use anymore
def removePrd(df):
    prdcd = df['Product Code'].dropna()
    prds = DATA_PRODUCT_MAPPING_LKP.query.filter(~DATA_PRODUCT_MAPPING_LKP.PRD_CD.in_(prdcd)).all()
    if prds:
        for p in prds:
            print('---------inactive prdcd: {} ---------'.format(p.PRD_CD))
            p.EFF_TO_DT = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            p.CRNT_F = 'N'
            p.UPDT_PROCESS_TMSTMP = datetime.timestamp(datetime.now())
        db.session.commit()



if __name__ == '__main__':
    print('starttime :',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    readProduct(dfp)
    removePrd(dfp)
    readCSV(dfa)
    readCredit(dfc)
    print('endtime :', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # then create view VW_RESD_MTGE_OA_RISK in mysql instead of create table RESD_MTGE_OA_RISK