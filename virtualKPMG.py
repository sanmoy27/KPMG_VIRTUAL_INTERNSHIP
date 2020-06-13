# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:22:34 2020

@author: OEACL68
"""

import warnings
warnings.filterwarnings('ignore')
import os
path="D:\\myProjects\\KPMG\\Code"
os.chdir(path)
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


transactionDF=pd.read_excel("../data/KPMG_rawData.xlsx", sheetname="Transaction")
newCustDF=pd.read_excel("../data/KPMG_rawData.xlsx", sheetname="NewCustomerList")
custDemoDF=pd.read_excel("../data/KPMG_rawData.xlsx", sheetname="CustomerDemographic")
custAddrDF=pd.read_excel("../data/KPMG_rawData.xlsx", sheetname="CustomerAddress")

def missing_values_table(df):
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table_ren_columns = mis_val_table.rename(
    columns = {0 : 'Missing Values', 1 : '% of Total Values'})
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
    '% of Total Values', ascending=False).round(1)
    
    print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
        "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")
    
    return mis_val_table_ren_columns

############ Transaction Table ########################
print(transactionDF.shape)
print(transactionDF.columns)
print(missing_values_table(transactionDF))
transactionDF.info()

transactionDF['transaction_date'] = pd.to_datetime(transactionDF['transaction_date'], unit='s')

transactionDF['online_order'].isnull().sum()
transactionDF['online_order'].value_counts()
transactionDF['online_order']=transactionDF['online_order'].fillna(1)
transactionDF['online_order']=transactionDF['online_order'].astype(int)

transactionDF['brand'].isnull().sum()
transactionDF['brand'].value_counts()
transactionDF['brand']=transactionDF['brand'].fillna('Solex')

transactionDF['product_line'].isnull().sum()
transactionDF['product_line'].value_counts()
transactionDF['product_line']=transactionDF['product_line'].fillna('Standard')

transactionDF['product_class'].isnull().sum()
transactionDF['product_class'].value_counts()
transactionDF['product_class']=transactionDF['product_class'].fillna('medium')

transactionDF['product_size'].isnull().sum()
transactionDF['product_size'].value_counts()
transactionDF['product_size']=transactionDF['product_size'].fillna('medium')

transactionDF['standard_cost'].isnull().sum()
avgCost=transactionDF.loc[transactionDF['standard_cost'].notnull()]
transactionDF['standard_cost']=transactionDF['standard_cost'].fillna(np.mean(avgCost['standard_cost']))


transactionDF['product_first_sold_date'].isnull().sum()
transactionDF['product_first_sold_date'].value_counts()
print(max(transactionDF['product_first_sold_date']))
transactionDF['product_first_sold_date']=transactionDF['product_first_sold_date'].fillna(max(transactionDF['product_first_sold_date']))
transactionDF['product_first_sold_date'] = pd.to_datetime(transactionDF['product_first_sold_date'], unit='s')



################# Clean Customer Demographics #######################
print(custDemoDF.shape)
print(custDemoDF.columns)
custDemoDF=custDemoDF.drop(columns=['default'])
print(missing_values_table(custDemoDF))

custDemoDF['gender'].value_counts()
custDemoDF['gender']=custDemoDF['gender'].replace({'Male':'M', 'Female':'F',
          'Femal':'F'})

custDemoDF['job_title'].isnull().sum()
custDemoDF['job_title'].value_counts()
custDemoDF['job_title']=custDemoDF['job_title'].fillna(method='bfill')

custDemoDF['job_industry_category'].isnull().sum()
custDemoDF['job_industry_category'].value_counts()
custDemoDF['job_industry_category']=custDemoDF['job_industry_category'].fillna(method='ffill')


custDemoDF['DOB'] = pd.to_datetime(custDemoDF['DOB'])
avgCustAge=custDemoDF.loc[(custDemoDF['DOB'].notnull()) & (custDemoDF['DOB']!='1843-12-21')]
avgCustAge['custAge']=pd.to_datetime('today')-avgCustAge['DOB']
avgCustAge['custAge']=avgCustAge['custAge'].dt.days.astype(int)
meanCustAge=round(np.mean(avgCustAge['custAge'])/365.5)

custDemoDF['CustAge'] = pd.to_datetime('today')-custDemoDF['DOB']
custDemoDF['CustAge']=custDemoDF['CustAge'].fillna(np.timedelta64(timedelta(days=meanCustAge)))
custDemoDF['CustAge']=custDemoDF['CustAge'].dt.days.astype(int)
custDemoDF['CustAge']=round(custDemoDF['CustAge']/365.5).astype(int)
custDemoDF['CustAge'].isnull().sum()
custDemoDF.loc[(custDemoDF['CustAge']==176) | (custDemoDF['CustAge']==0), ['CustAge']]=meanCustAge

def calCustAgeBuckets(age):
    if age.CustAge>=18 and age.CustAge<=30:
        return '18-30'
    elif age.CustAge>30 and age.CustAge<=40:
        return '31-40'
    elif age.CustAge>40 and age.CustAge<=50:
        return '41-50'
    elif age.CustAge>50 and age.CustAge<=60:
        return '51-60'
    else:
        return '>60'

custDemoDF['CustAgeBuckets'] = custDemoDF.apply(calCustAgeBuckets, axis=1)
custDemoDF['CustAgeBuckets'].value_counts()


custDemoDF['tenure'].isnull().sum()
custDemoDF['tenure'].value_counts()
avgTenure=custDemoDF.loc[(custDemoDF['tenure'].notnull())]
meanTenure=round(np.mean(avgTenure['tenure']))
custDemoDF['tenure']=custDemoDF['tenure'].fillna(meanTenure)

custDemoDFv1 = custDemoDF[['customer_id', 'gender',
       'past_3_years_bike_related_purchases', 'job_title',
       'job_industry_category', 'wealth_segment', 'deceased_indicator',
       'owns_car', 'tenure', 'CustAgeBuckets']]
print(missing_values_table(custDemoDFv1))

print(missing_values_table(custAddrDF))

########## Combine Customer Demographics and customer address
custDemoDFv2 = pd.merge(custDemoDFv1, custAddrDF, on="customer_id", how="left")
custDemoDFv3 = custDemoDFv2[['customer_id', 'gender',
       'past_3_years_bike_related_purchases', 'job_title',
       'job_industry_category', 'wealth_segment', 'deceased_indicator',
       'owns_car', 'tenure', 'CustAgeBuckets', 'property_valuation']]

print(missing_values_table(custDemoDFv3))

custDemoDFv3['property_valuation'].isnull().sum()
custDemoDFv3['property_valuation'].value_counts()
avgProperty=custDemoDFv3.loc[(custDemoDFv3['property_valuation'].notnull())]
meanProperty=round(np.mean(avgProperty['property_valuation']))
custDemoDFv3['property_valuation']=custDemoDFv3['property_valuation'].fillna(meanProperty)


############ Combine Transaction Table
cust_transaction = pd.merge(custDemoDFv3, transactionDF, on="customer_id", how="inner")
cust_transaction['Profit'] = cust_transaction['list_price'] - cust_transaction['standard_cost']

print(missing_values_table(cust_transaction))

pivoted_brand = pd.pivot_table(cust_transaction, index=['customer_id'], columns=["brand"], values=["product_id"], aggfunc={"product_id":len}, fill_value=0)
#flattened_brand = pd.DataFrame(pivoted_brand.to_records())
pivoted_brand.columns = pivoted_brand.columns.droplevel(0)
pivoted_brand.columns.name = None               
pivoted_brand = pivoted_brand.reset_index() 


pivoted_productLine = pd.pivot_table(cust_transaction, index=['customer_id'], columns=["product_line"], values=["product_id"], aggfunc={"product_id":len}, fill_value=0)
pivoted_productLine.columns = pivoted_productLine.columns.droplevel(0)
pivoted_productLine.columns.name = None               
pivoted_productLine = pivoted_productLine.reset_index() 


pivoted_productClass = pd.pivot_table(cust_transaction, index=['customer_id'], columns=["product_class"], values=["product_id"], aggfunc={"product_id":len}, fill_value=0)
pivoted_productClass.columns = pivoted_productClass.columns.droplevel(0)
pivoted_productClass.columns.name = None               
pivoted_productClass = pivoted_productClass.reset_index() 

max_tranDate = cust_transaction.groupby(["customer_id"]).agg({'transaction_date': [np.max]})
max_tranDate.columns = max_tranDate.columns.droplevel(0)
max_tranDate.columns.name = None               
max_tranDate = max_tranDate.reset_index() 

sum_profit = cust_transaction.groupby(["customer_id"]).agg({'Profit': [np.sum]})
sum_profit.columns = sum_profit.columns.droplevel(0)
sum_profit.columns.name = None               
sum_profit = sum_profit.reset_index()

total_tran = cust_transaction.groupby(["customer_id"]).agg({'customer_id': ['count']})
total_tran.columns = total_tran.columns.droplevel(0)
total_tran.columns.name = None               
total_tran = total_tran.reset_index()
total_tran = total_tran.rename(columns={'count':'total_transaction'})


online_tran = cust_transaction.groupby(["customer_id"]).agg({'online_order': [np.sum]})
online_tran.columns = online_tran.columns.droplevel(0)
online_tran.columns.name = None               
online_tran = online_tran.reset_index()
online_tran = online_tran.rename(columns={'sum':'total_online_transaction'})

#pd.DataFrame({"customer_id":cust_transaction["customer_id"].unique()})
unique_rec = cust_transaction[['customer_id', 'gender', 'past_3_years_bike_related_purchases',
       'job_title', 'job_industry_category', 'wealth_segment',
       'deceased_indicator', 'owns_car', 'tenure', 'CustAgeBuckets',
       'property_valuation']]

unique_rec = unique_rec.drop_duplicates()

df = pd.merge(unique_rec, max_tranDate, on="customer_id", how="left")
df1 = pd.merge(df, pivoted_brand, on="customer_id", how="left")
df2 = pd.merge(df1, sum_profit, on="customer_id", how="left")
df3 = pd.merge(df2, online_tran, on="customer_id", how="left")
df4 = pd.merge(df3, total_tran, on="customer_id", how="left")


df4 = df4.rename(columns={'amax':'max_transaction_date', 'sum':'sum_profit'})
df4.to_excel("../Analysis/df4.xlsx", index=False)
cust_transaction.to_excel("../Analysis/cust_transaction.xlsx", index=False)