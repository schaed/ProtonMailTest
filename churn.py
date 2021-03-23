import pandas as pd
import matplotlib.pyplot as plt
draw=True
verbose=False
def GetInvoicesPerCustomer(df_all_customers,df):
    df_customer_invoice = df.groupby(['Customer ID','Invoice','InvoiceDate'], dropna=True).sum()
    dfID = {}
    for ide in df_all_customers:
        dfID[ide] = [len(df_customer_invoice[df_customer_invoice.index.get_level_values(0)==ide])]
    return pd.DataFrame.from_dict(dfID, orient='index', columns=['Invoices'])

df = pd.read_csv('online_combined.csv')
df['InvoiceDate'] = pd.to_datetime(df.InvoiceDate)

# add the total amount spent
df['totalcost'] = df['Price']*df['Quantity']

# The church rate for the second half of 2011 is 47%. This is 2366 customers.
# customers before June 2011
mask = (df['InvoiceDate'] < '2011-6-1')
df_beforeJune2011=df.loc[mask]
mask = (df['InvoiceDate'] >= '2011-6-1')
df_afterJune2011=df.loc[mask]

# build list of customers before June 2011.
df_before_customers = df_beforeJune2011['Customer ID'].unique()
df_all_customers = df['Customer ID'].unique()
df_after_customers = df_afterJune2011['Customer ID'].unique()
n_before_customers = len(df_before_customers)
print('')
print('Total customers before June 2011: %s' %n_before_customers)
print('Total customers after June 2011: %s' %len(df_after_customers))
print('')
# Compute the churn rate
churn_customers=0
new_customers=0
for ide in df_before_customers:
    if not (ide in df_after_customers):
        churn_customers+=1
for ide in df_after_customers:
    if not (ide in df_before_customers):
        new_customers+=1
print('')
print('Churned customers: %s new customers: %s Churn rate: %s' %(churn_customers,new_customers, 100*(churn_customers/n_before_customers)))
print('')
# If we select customers who have more than 1 invoice, then the churn rate is 37%
print('If we select customers who have more than 1 invoice, then the churn rate is 37\%')
df_ID_Ninvoice        = GetInvoicesPerCustomer(df_all_customers,df)
df_ID_Ninvoice_before = GetInvoicesPerCustomer(df_before_customers,df_beforeJune2011)
df_ID_Ninvoice_after  = GetInvoicesPerCustomer(df_after_customers,df_afterJune2011)
if verbose:
    print(df_ID_Ninvoice)
churn_customers_mto=0
customers_more_than_oneInv_before = df_ID_Ninvoice_before[df_ID_Ninvoice_before['Invoices']>1].index.unique()
n_customers_more_than_oneInv_before = len(customers_more_than_oneInv_before)
for ide in customers_more_than_oneInv_before:
    if not (ide in df_after_customers):
        churn_customers_mto+=1        
print('')
print('Customers with more than 1 Invoice rates - Churned customers: %s Churn rate: %s' %(churn_customers_mto, 100*(churn_customers_mto/n_customers_more_than_oneInv_before)))
print('')
# Are there customers close to churning? Going back to all customers and not just the ones with more than one invoice prior to June 2011. This I plot as the time since their last invoice, and I plot it as the number versus the month
print('Are there customers close to churning? Going back to all customers and not just the ones with more than one invoice prior to June 2011. This I plot as the time since their last invoice, and I plot it as the number versus the month')
i = pd.date_range('2011-06-01', periods=6, freq='1M')
df_customer_invoice_after = df_afterJune2011.groupby(['Customer ID','Invoice','InvoiceDate'], dropna=True).sum()
if verbose:
    print(df_customer_invoice_after)
lastInvoice = []
for ide in df_before_customers:
    if ide in df_after_customers:
        df_thiscustomer = df_customer_invoice_after[df_customer_invoice_after.index.get_level_values(0)==ide] #['InvoiceDate'][-1]
        last_invoice =df_thiscustomer.index.get_level_values(2).sort_values()[-1]
        lastInvoice+=[last_invoice]
        # if you want to print customers at risk of churning, then
        if last_invoice.month<9 and verbose:
            print('Last purchase was before september. At risk of churning: %s' %ide)
monthly_last_invoice=[]
timeList=[]
for d in i:
    timeList+=[d]
    nmonth=0
    for itime in lastInvoice:
        if d.month==itime.month:
            nmonth+=1
    monthly_last_invoice+=[nmonth]

# Customers who have not ordered since July, August, or September are from highest to lowest priority to churn. A targeted campaign to advertise to only these customers could be put together. Trying to encourage them to buy, especially near the December holidays. Fortunately, the number of customers with their last invoice in July-September is small compared to those more recent. However, the orders are very holiday driven with more invoices near the December.
print('')
print('Customers who have not ordered since July, August, or September are from highest to lowest priority to churn. A targeted campaign to advertise to only these customers could be put together. Trying to encourage them to buy, especially near the December holidays. Fortunately, the number of customers with their last invoice in July-September is small compared to those more recent. However, the orders are very holiday driven with more invoices near the December.')
if draw:
    plt.plot(list(timeList),list(monthly_last_invoice))
    plt.gcf().autofmt_xdate()
    plt.ylabel('Number of Prior Customers')
    plt.xlabel('Month of Last Invoice')
    plt.show()
        
