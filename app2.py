from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import numpy as np
import io
import csv
import os

app = Flask(__name__)

# Listening for GET requests to the root URL
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index2.html')

# The function that creates groups from the CSV file
def intoGroup(xlsx_file, no_of_groups):
    # Delete the old CSV file if it exists
    if os.path.exists("new2.csv"):
        os.remove("new2.csv")
    
    # Delete the old XLSX file if it exists
    if os.path.exists("new2.xlsx"):
        os.remove("new2.xlsx")
    
    # Save the uploaded XLSX file
    xlsx_file.save("new2.xlsx")

    # Read the xlsx file
    df = pd.read_excel("new2.xlsx", engine='openpyxl')

    # Shuffle the rows randomly
    df = df.sample(frac=1).reset_index(drop=True)

    # Divide the data into equally-sized groups
    group_size = len(df) // no_of_groups
    groups = [df[i:i+group_size] for i in range(0, len(df), group_size)]

    # Make sure that the last group has the remaining rows if the number of rows is not evenly divisible by no_of_groups
    if len(groups) != no_of_groups:
        groups[-1] = groups[-1].append(df[len(groups)*group_size:])
    
    # Iterate through the groups and assign a group number to each row
    for i, group in enumerate(groups):
        group["group"] = i+1

    # Concatenate the groups back into a single DataFrame and save the result to a CSV file
    result = pd.concat(groups)
    result.to_csv("new2.csv", index=False)

    return result


# Listening for POST requests to the '/upload' URL
@app.route('/upload', methods=['POST'])
def upload():
    no_of_groups = int(request.form['no_of_groups'])
    xlsx_file = request.files['file']
    result = intoGroup(xlsx_file, no_of_groups)
    return send_file(io.BytesIO(result.to_csv().encode()), mimetype='text/csv', attachment_filename='new2.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
