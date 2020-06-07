# dashboard_generator.py


import pandas as pd
import os
import numpy
import tkinter as tk
from tkinter import filedialog
import re
import matplotlib as plot
import matplotlib.pyplot as plt
import altair as alt 
from altair import Chart, X, Y, Axis, SortField

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

#prompt the user for a file see https://www.youtube.com/watch?v=H71ts4XxWYU
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

#validate the file and quit if does not meet sales file regex condition
validatethis = file_path[-16:]
if re.match(r"^(sales)-[0-9][0-9][0-9][0-9][0-9][0-9].(csv)", validatethis):
    print()
else:
    print('This is not a valid file. Please select a monthly sales file.')
    exit()

#create dataframe from selected file
df = pd.read_csv(file_path, error_bad_lines=False)

#create column for month and year of sales report
df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month
df['monthname'] = pd.to_datetime(df['month'], format='%m').dt.month_name()
#get month name as variable
month = df.at[0,'monthname']
#get year as variable
year = df.at[0,'year']
#calculate revenue
revenue = df["sales price"].sum() 
df["formattedrevenue"] = to_usd(revenue)
print(df)
#print beginning of report
print("-----------------------")
print("MONTH:" + ' ' + str(month) + ' ' + str(year))
print("-----------------------")
print("CRUNCHING THE DATA...")
print("-----------------------")
#print("TOTAL MONTHLY SALES: $12,000.71")
print("TOTAL MONTHLY SALES:",to_usd(revenue))

#identify Top selling products:
#create new df of items with the max units sold
pdsales = df.groupby(['product'], as_index=False).sum()
pdsales["revenue"] = pdsales["sales price"]
#make the column be in USD
pdsales["formattedrevenue"] = pdsales["revenue"].apply(to_usd)
print(pdsales)
#sort them by top sellers
pdsalessorted = pdsales.sort_values(by=['revenue'], ascending=False)

#add column with number of rows, to list out later. plus 1 is necessary as lists start at 0. :)
pdsalessorted["number"] = numpy.arange(len(pdsalessorted)) + 1

#iterate through and print the number in popularity, product name and total revenue
print("-----------------------")
print("TOP SELLING PRODUCTS:")
for index, row in pdsalessorted.iterrows():
    print(row['number'],row['product'],row['formattedrevenue'])

print(pdsalessorted)
print(type(pdsalessorted))

#DATA VISUALIZATION

print("-----------------------")
print("VISUALIZING THE DATA...")


newdf = pdsalessorted.filter(['product','revenue','formattedrevenue'], axis=1)
print(newdf)
rev = newdf.at[0,'revenue']
print(type(rev))



productname = newdf['product'].tolist()
revenueamt = newdf['revenue'].tolist()
formattedrevenueamt = newdf['formattedrevenue'].tolist()
#productname = []
#revenueamt = []
#for x in newdf:
#    productname.append(x['product'])
#    revenueamt.append(x['revenue'])
print(productname)
#print(revenueamt)
print(formattedrevenueamt)


x = [i for i in productname]
rev = [i for i in revenueamt]

x_pos = [i for i, _ in enumerate(x)]

plt.barh(x_pos, rev, color='green')
plt.ylabel("Product")
plt.xlabel("Revenue ($)")
plt.title("Top Selling Products" + ' ' + str(month) + ' ' + str(year))

plt.yticks(x_pos, x)

plt.show()




#newdf.T.to_dict().values()
#print(newdf)
#newdf.to_dict('records')
#print(records)
#newdf.plot.bar()
#newdf['formattedrevenue'].hist()

#newdf.plot(kind="bar", x=pdsalessorted['product'], title="Sales",legend=False)


#pdsalessorted.plot(kind="bar", x=pdsalessorted["product"], title="Sales",legend=False)

#alt.Chart(pdsalessorted).mark_bar().encode(x='product',y='revenue')

#pdsalessorted.plot.bar(x='product', y='revenue', title="Monthly sales by product")
#plot.show(block=True)

#bar_data = pdsalessorted
#x = [i["product"] for i in bar_data]
#viewers = [i["formattedrevenue"] for i in bar_data]
#x_pos = [i for i, _ in enumerate(x)]
#plt.barh(x_pos, viewers, color='green')


#print(bar_data)
