import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
draw=True
verbose=False
def Download():
    # Download the input file
    import urllib.request
    urllib.request.urlretrieve('http://archive.ics.uci.edu/ml/machine-learning-databases/00502/online_retail_II.xlsx','online_retail_II.xlsx')
    urllib.request.urlretrieve('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx','online_retail.xlsx')

def ConvertCsv():
    print('downloading the data...')
    Download()
    print('Reading in the data...')
    df=pd.read_excel('online_retail_II.xlsx')
    df2=pd.read_excel('online_retail.xlsx')
    # make sure to harmonize the data columns
    df2.columns=['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate','Price', 'Customer ID', 'Country']

    df3 = pd.concat([df,df2])
    df3.to_csv('online_combined.csv')

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


# reading xlxs is very slow, so we convert this to csv
if not os.path.exists('online_combined.csv'):
    ConvertCsv()
    
df = pd.read_csv('online_combined.csv')
if verbose:
    print (df)
# Fix column type
df['InvoiceDate'] = pd.to_datetime(df.InvoiceDate)
if verbose:
    print (df.sort_values(by='InvoiceDate'))
#print the column names
if verbose:
    print(df.columns)

# add the total amount spent
df['totalcost'] = df['Price']*df['Quantity']

# Check for other null entries by column. The rest is corrupted data and would exclude for future analysis.
print('')
print('Check for other null entries by column. The rest is corrupted data and would exclude for future analysis.')
for c in df.columns:
    print('Column: %s and the number corrupted: %s' %(c, df[c].isnull().sum()))

# Fill the null users to check how big they are overall
# also noted that some of the descriptions are corrupted. Given this is a short project and the size is small, I will ignore any corrupted item descriptions.
print('')
print('Fill the null users to check how big they are overall')
print('also noted that some of the descriptions are corrupted. Given this is a short project and the size is small, I will ignore any corrupted item descriptions.')
df['nullID']=df['Customer ID'].isnull()

# brief summary for future analysis. I wanted to know how many users IDs are missing
print('')
print('Brief summary for future analysis. I wanted to know how many users IDs are missing as well as how many customers, items, and invoices there are. ')
print('Unique purchases: %s' %(len(df['Description'].unique())))
print('Unique customers: %s' %(len(df['Customer ID'].unique())))
print('Unregistered purchases: %s' %(len(df[df['nullID']==True]['Invoice'].unique())))
print('Unique Invoices: %s' %(len(df['Invoice'].unique())))


# Grouping by invoice for later analysis. I'm trying to get a feeling for how often users purchase and how much.
print('')
print('Grouping by invoice for later analysis. I am trying to get a feeling for how often users purchase and how much.')
invoice_group = df.groupby(['Invoice']).sum()
if verbose:
    print(invoice_group)

# Drawing the number of items purchased per invoice including returns to see the typical size.
# Number of items can be very large. For the very large number of items, For the order with more than 87000  are typically
# I want to see what was cancelled with more than 75000 items. The costumer is 642465.0. Given this very large order, I would recommend reaching out to this customer to see if they could be better served. Let them know that they are valued.
print(' Drawing the number of items purchased per invoice including returns to see the typical size.')
print(' Number of items can be very large. For the very large number of items, For the order with more than 87000  are typically')
print(' I want to see what was cancelled with more than 75000 items. The costumer is 642465.0. Given this very large order, I would recommend reaching out to this customer to see if they could be better served. Let them know that they are valued.')
if draw:
    plt.hist(invoice_group['Quantity'],bins=100, log=True)
    plt.xlabel('Number of Items / Invoice')
    plt.ylabel('Items purchased')
    plt.show()
    
# I want to see what was cancelled with more than 75000 items
print('')
print('I want to see what was cancelled with more than 75000 items. It was one customer.')
print(invoice_group[invoice_group['Quantity']<-50000])
# has this customer ordered many times?
print('')
print('has this customer ordered many times? Below is their list of orders for Customer ID 642465.0')
cust_id = invoice_group[invoice_group['Customer ID']==642465.0]

print('')
print(' printing the list of orders')
print(' This customer only ordered once and cancelled their order. Given the size of this order, I would reach out to this person to find out what shaped their decision and to see if something would change their mind about cancelling.')
# printing the list of orders
# This customer only ordered once and cancelled their order. Given the size of this order, I would reach out to this person to find out what shaped their decision and to see if something would change their mind about cancelling.
print(cust_id)

# The real target customers are those who have made very large orders. There are 4 cancellations with total order cost of more than 20k pounds.
if draw:
    plt.hist(invoice_group['totalcost']/1.0e3,bins=100, log=True)
    plt.xlabel('Total Invoice [thousands of pounds]')
    plt.ylabel('Invoices')
    plt.show()
# Many of these large cancellations are from new customers. Might want to double check the quantity with the user before they finish their order? Perhaps the website can be improved
print('')
print('Many of these large cancellations are from new customers. Might want to double check the quantity with the user before they finish their order? Perhaps the website can be improved')
print('')
print('Printing invoices with more than 20k pounds worth returned')
print(invoice_group[invoice_group['totalcost']<-20e3])
print('')
print('Printing invoices more than 10k pounds worth returned')
print(invoice_group[invoice_group['totalcost']<-10e3])    
    
# How many purchases has the same customer made? This distribution is useful for defining boundaries for classes of customers based upon their number of items purchased
df_unique_customer_rmNan=df.groupby(['Customer ID'], dropna=True).size()
df_unique_customer=df.groupby(['Customer ID'], dropna=False).size()
if verbose:
    print(df_unique_customer.sum())
if draw:
    plt.hist(df_unique_customer_rmNan,bins=100)
    plt.xlabel('Number of Items Purchased / Customer')
    plt.ylabel('Purchases')
    plt.show()

# I divide the customers into the number of of items purchased. This is useful to see the distribution with fewer categories of customers. This grouping could be used potentially to define levels of customers for rewards, which I discuss more below.
# In this distribution, I note the very small number of customers who have made more than 500 purchases. The next distribution is to look at the gross revenue from these different categories of customers.
# 1st time customers are pretty low, which means that customers very often make additional orders. It might be worth surveying to understand why the 1st time customers were unhappy.
print('')
print('')
print(' I divide the customers into the number of of items purchased. This is useful to see the distribution with fewer categories of customers. This grouping could be used potentially to define levels of customers for rewards, which I discuss more below.')
print(' In this distribution, I note the very small number of customers who have made more than 500 purchases. The next distribution is to look at the gross revenue from these different categories of customers.')
print(' 1st time customers are pretty low, which means that customers very often make additional orders. It might be worth surveying to understand why the 1st time customers were unhappy.')
print('')
print('splitting customers based upon their number of orders')
numberOfOrders={}
numberOfOrders['1st Time']=(df_unique_customer.between(0,1, inclusive=True)).sum()
numberOfOrders['2-10']=(df_unique_customer.between(2,10, inclusive=True)).sum()
numberOfOrders['11-49']=(df_unique_customer.between(11,49, inclusive=True)).sum()
numberOfOrders['50-99']=(df_unique_customer.between(50,99, inclusive=True)).sum()
numberOfOrders['100-499']=(df_unique_customer.between(100,499, inclusive=True)).sum()
numberOfOrders['>500']=(df_unique_customer.between(500,500000, inclusive=True)).sum()
if verbose:
    print(list(numberOfOrders.keys()))
    print(list(numberOfOrders.values()))
if draw:
    fig = plt.figure(figsize = (10, 5))
    plt.bar( list(numberOfOrders.keys()),list(numberOfOrders.values()))
    plt.xlabel('Number of Items')
    plt.ylabel('Number of Customers')
    plt.show()

# Beyond the types of customers, the revenue broken down by number of customer orders is shown.
# Customers with more than 100 orders make up 82% of the total revenue. The customers with more than 500 orders have a gross revenue of more than 2 million pounds. 
#  We need to make sure to keep these repeat customers with more than 100 orders happy and especially those with more than 500 orders
# Grouping by their number number of items is a good way to target consumers. Better deals should be targeted at consumers with more than 100 orders to keep them coming back.
# First time users are also a group to continue to grow.

print(' Beyond the types of customers, the revenue broken down by number of customer orders is shown.')
print(' Customers with more than 100 orders make up 82% of the total revenue. The customers with more than 500 orders have a gross revenue of more than 2 million pounds. ')
print(' We need to make sure to keep these repeat customers with more than 100 orders happy and especially those with more than 500 orders')
print(' Grouping by their number number of items is a good way to target consumers. Better deals should be targeted at consumers with more than 100 orders to keep them coming back.')
print(' First time users are also a group to continue to grow.')
rev={}
rev_selection = [['1st Time',0,1],['2-10',2,10],['11-49',11,49],['50-99',50,99],['100-499',100,499],['>500',500,5000000]]
df_unique_customer_rmNan_rev= df.groupby(['Customer ID'], dropna=True).sum()
if verbose:
    print(df_unique_customer_rmNan_rev)
for revsel in rev_selection:
    rev[revsel[0]]=0 # initialize
    for i in df_unique_customer[df_unique_customer.between(revsel[1],revsel[2], inclusive=True)].index:
        rev[revsel[0]]+=df_unique_customer_rmNan_rev[df_unique_customer_rmNan_rev.index==i]['totalcost'].sum()/1.0e6
if draw:
    fig = plt.figure(figsize = (10, 5))
    plt.bar( list(rev.keys()),list(rev.values()))
    plt.xlabel('Customer - Number of Items')
    plt.ylabel('Total Purchased Rev. in Millions of Pounds')
    plt.show()
    print('Total Revenue from >100 orders: %s' %((rev['>500']+rev['100-499'])/sum(rev.values())))

# See where the revenue per country
# More than 90% of the revenue is coming from the UK. There are smaller orders from a lot of countries.
# If looking to expand from the UK (although this would need to be investigated with Brexit), then the EIRE, Netherlands, Germany, and France would be the best places to start advertising
print(' See where the revenue per country')
print(' More than 90% of the revenue is coming from the UK. There are smaller orders from a lot of countries.')
print(' If looking to expand from the UK (although this would need to be investigated with Brexit), then the EIRE, Netherlands, Germany, and France would be the best places to start advertising')
orders_by_country = df.groupby(['Country'], dropna=True).sum().sort_values(by='totalcost')[-6:]
orders_by_country_other = df.groupby(['Country'], dropna=True).sum().sort_values(by='totalcost')[:-7]['totalcost'].sum()
if verbose:
    print(orders_by_country)
if draw:
    fig = plt.figure(figsize = (10, 5))
    plt.bar( list(['Other'])+list(orders_by_country.index),list(list([orders_by_country_other/1.0e6])+list(orders_by_country['totalcost']/1.0e6)))
    plt.xlabel('Country')
    plt.ylabel('Total Revenue')
    plt.show()
    print('Total Revenue from >100 orders: %s' %((rev['>500']+rev['100-499'])/sum(rev.values())))
    
# How many items are ordered per month? Same for revenue. This code draws these distributions
print('')
print(' How many items are ordered per month? Same for revenue. This code draws these distributions')
monthly = df.groupby(pd.Grouper(key = 'InvoiceDate', freq='1M'), dropna=True).sum()

itime = pd.date_range('2009-12-01', periods=24, freq='1M')
time=[]
monthly_rev = []
monthly_tot = []
if verbose:
    print(monthly['totalcost'])
j=0
for d in itime:
    monthly_tot+=[monthly['Quantity'][j]/1.0e5]
    monthly_rev+=[monthly['totalcost'][j]/1.0e6]
    time+=[d]
    j+=1

# The number of items ordered increased greatly near December for holiday purchases. More staff may be needed to process these orders
# The peak number of items ordered is also increasing from Dec 2011 to Dec 2012. April is lower in 2011 than 2010, which might be interesting to investigate further
print('')
print('The number of items ordered increased greatly near December for holiday purchases. More staff may be needed to process these orders')
print(' The peak number of items ordered is also increasing from Dec 2011 to Dec 2012. April is lower in 2011 than 2010, which might be interesting to investigate further')
if verbose:
    print(monthly_rev)
if draw:
    plt.plot(list(time),list(monthly_tot))
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    plt.ylabel('Number of items purchased [per 100k]')
    plt.xlabel('Month')
    plt.show()

# Total revenue is also strongly peaked starting in October through January. The difference in April 2010 versus April 2011 is gone, which may be an artifact of the large cancelled orders
print('Total revenue is also strongly peaked starting in October through January. The difference in April 2010 versus April 2011 is gone, which may be an artifact of the large cancelled orders')
if verbose:
    print(monthly_rev)
if draw:
    plt.plot(list(time),list(monthly_rev))
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    #plt.hist(monthly['Quantity'],bins=100, log=True)
    plt.ylabel('Total Revenue in Millions of Pounds')
    plt.xlabel('Month')
    plt.show()    

# Drawing the number of items per invoice. Again large numbers of items in a single invoice might be a concern for cancelled orders
print('')
print('Drawing the number of items per invoice. Again large numbers of items in a single invoice might be a concern for cancelled orders, which show up as negative entries.')
if draw:
    plt.hist(invoice_group['Quantity'],bins=100, log=True)
    plt.xlabel('Number of Items / Invoice')
    plt.ylabel('Items purchased')
    plt.show()

