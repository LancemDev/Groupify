# from flask import Flask, render_template, request, send_file
import pandas as pd

no_of_groups = 5
xlsx_file = "ICSA.xlsx"

# The function that creates groups from the Excel file
def intoGroup(xlsx_file, no_of_groups):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(xlsx_file, engine='openpyxl')

    # Shuffle the rows randomly
    df = df.sample(frac=1).reset_index(drop=True)

    # Divide the data into equally-sized groups
    no_of_groups = len(df) // no_of_groups
    groups = [df[i:i+no_of_groups] for i in range(0, len(df), no_of_groups)]

    # Make sure that the last group has the remaining rows if the number of rows is not evenly divisible by the number of groups

    groups[-1] = pd.concat([groups[-1],df[len(groups)*no_of_groups:]]).reset_index(drop=True)

    # Iterate through the groups and assign a group number to each row
    for i, group in enumerate(groups):
        group["Group"] = i+1

    # Concatenate the groups back into a single DataFrame
    result = pd.concat(groups)

    # Save the result to an Excel file
    result.to_excel("new2.xlsx", index=False)

    return result

# The resulting excel file to be downloaded
result = intoGroup(xlsx_file, no_of_groups)