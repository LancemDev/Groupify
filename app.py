from flask import Flask, render_template, request, send_file
import pandas as pd
import io
import os

app = Flask(__name__)

# Listening for GET requests to the root URL
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# The function that creates groups from the CSV file
# The function that creates groups from the Excel file
def intoGroup(xlsx_file, no_of_groups):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(xlsx_file)

    # Shuffle the rows randomly
    df = df.sample(frac=1).reset_index(drop=True)

    # Divide the data into equally-sized groups
    group_size = len(df) // no_of_groups
    groups = [df[i:i+group_size] for i in range(0, len(df), group_size)]

    # Make sure that the last group has the remaining rows if the number of rows is not evenly divisible by the number of groups
    groups[-1] = groups[-1].append(df[len(groups)*group_size:])

    # Iterate through the groups and assign a group number to each row
    for i, group in enumerate(groups):
        group["group"] = i+1

    # Concatenate the groups back into a single DataFrame
    result = pd.concat(groups)

    # Save the result to an Excel file
    result.to_excel("new2.xlsx", index=False)

    return result


# Listening for POST requests to the '/upload' URL
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    no_of_groups = request.form.get('no_of_groups')
    if no_of_groups is not None:
        no_of_groups = int(no_of_groups)
    xlsx_file = request.files.get('my-awesome-dropzone')
    final = intoGroup(xlsx_file, no_of_groups)
    return send_file("new2.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
