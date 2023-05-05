from os import sendfile
from flask import Flask, request, jsonify, render_template
import pandas as pd 
import numpy as np
#import openpyxl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template ('dropdown.html')

def intoGroup(xlsx_file, no_of_groups):
    #convert the xlx file to csv
    df = pd.read_excel(xlsx_file)
    df = df.to_csv('icsd _comm_skills.csv', index=False)

    # Shuffle the rows randomly
    df = df.sample(frac=1).reset_index(drop=True)

    # Divide the data into 8 equally-sized groups
    group_size = no_of_groups // no_of_groups
    groups = [df[i:i+group_size] for i in range(0, no_of_groups, group_size)]

    # Make sure that the last group has the remaining rows if the number of rows is not evenly divisible by the input number of groups
    groups[-1] = groups[-1].append(df[no_of_groups-len(groups[-1]):])

    # Iterate through the groups and assign a group number to each row
    for i, group in enumerate(groups):
        group["group"] = i+1

    # Concatenate the groups back into a single DataFrame and save the result to a CSV file
    result = pd.concat(groups)
    result.to_csv("first_web_result.csv", index=False)

    #convert the csv file to xlsx
    read_file = pd.read_csv (r'first_web_result.csv')
    read_file = read_file.to_excel (r'first_web_result.xlsx', index = None, header=True)

    if None:
        return "File not uploaded"
    return read_file




@app.route('/file-upload', methods=['POST', 'GET'])
def file_upload():
    if request.method == 'POST':
        xls_file = request.files.get('my-awesome-dropzone')
        no_of_groups = request.form.get('no_of_groups')
        result = intoGroup(xls_file, no_of_groups)
        #return jsonify({'message': 'File uploaded successfully'})
        return render_template ('index.html', result = result)
    render_template ('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)