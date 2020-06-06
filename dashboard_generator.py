# dashboard_generator.py


import pandas as pd
import os
import numpy
import tkinter as tk
from tkinter import filedialog
import re


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
print(file_path)
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

#sort them by top sellers
pdsalessorted = pdsales.sort_values(by=['revenue'], ascending=False)

#add column with number of rows, to list out later. plus 1 is necessary as lists start at 0. :)
pdsalessorted["number"] = numpy.arange(len(pdsalessorted)) + 1

#iterate through and print the number in popularity, product name and total revenue
print("-----------------------")
print("TOP SELLING PRODUCTS:")
for index, row in pdsalessorted.iterrows():
    print(row['number'],row['product'],row['formattedrevenue'])

print("-----------------------")
print("VISUALIZING THE DATA...")

