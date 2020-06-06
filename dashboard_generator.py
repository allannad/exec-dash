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

#prompt the user for a file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

#validate the file and quit if does not meet condition
print(file_path)
validatethis = file_path[-16:]
if re.match(r"^(sales)-[0-9][0-9][0-9][0-9][0-9][0-9].(csv)", validatethis):
    print('Thank you for selecting the sales file')
else:
    print('This is not a valid file')
    exit()





print("-----------------------")
print("MONTH: March 2018")

print("-----------------------")
print("CRUNCHING THE DATA...")

print("-----------------------")
print("TOTAL MONTHLY SALES: $12,000.71")

print("-----------------------")
print("TOP SELLING PRODUCTS:")
print("  1) Button-Down Shirt: $6,960.35")
print("  2) Super Soft Hoodie: $1,875.00")
print("  3) etc.")

print("-----------------------")
print("VISUALIZING THE DATA...")

