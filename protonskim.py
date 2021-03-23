import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
#from pyspark import spark
df2=pd.read_excel('online_retail.xlsx')
print(df2)
print(df2.columns)
df2.columns=['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate','Price', 'Customer ID', 'Country']
print('')
df=pd.read_excel('online_retail_II.xlsx')
print(df)
print(df.columns)
df3 = pd.concat([df,df2])
df3.to_csv('myfilev2.csv')
sys.exit(0)
if True:
    df=pd.read_excel('online_retail_II.xlsx')
    df2=pd.read_excel('online_retail.xlsx')
    df3 = pd.concat([df,df2])
    df3.to_csv('myfilev2.csv')
#df3.write.csv("myfile.csv")
df4 = pd.read_csv('myfile.csv')
print(df4)
#df4 = spark.read.format("myfile.csv")
#print(df4)
#df3.to_csv('myfile.csv')
#df.printSchema()

#df = pd.read_excel('online_retail_II.xlsx')
sys.exit(0)
df = pd.read_excel('online_detail_1.xlsx')
for d in df['Description'].unique():
    print(d)
print (df.sort_values(by='InvoiceDate'))
print(df[-1:])
print(len(df))
print(df.count())
#df[-50000:].to_excel("online_retail_II_last50k.xlsx")


