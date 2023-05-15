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


# Listening for POST requests to the '/upload' URL
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    
    ALLOWED_EXTENSIONS = {'xlsx'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    uploaded_file = request.files.get('file')
    uploaded_file.save("data1.xlsx")
    no_of_groups = request.form.get('no_of_groups')
      
    if uploaded_file is None or not allowed_file(uploaded_file.filename):
        return 'Invalid file. Please upload an Excel file (xlsx).'
    
    if no_of_groups is not None:
        no_of_groups = int(no_of_groups)
    else:
        return 'No number of groups provided.'
        
    final = intoGroup(uploaded_file, no_of_groups)

    return send_file("new2.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
