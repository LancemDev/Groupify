from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd

app = Flask(__name__)


# Listening for GET requests to the root URL
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# The function that creates groups from the CSV file
def intoGroup(xlsx_file, no_of_groups):
    #Read the xlxs file and convert it to csv
    df = pd.read_excel(xlsx_file)
    df = df.to_csv('icsd _comm_skills.csv', index=False)

    # Shuffle the rows randomly
    df = df.sample(frac=1).reset_index(drop=True)

    # Divide the data into 8 equally-sized groups
    group_size = len(df) // 13
    groups = [df[i:i+group_size] for i in range(0, no_of_groups, group_size)]

    # Make sure that the last group has the remaining rows if the number of rows is not evenly divisible by 8
    groups[-1] = groups[-1].append(df[no_of_groups-len(groups[-1]):])


    # Iterate through the groups and assign a group number to each row
    for i, group in enumerate(groups):
        group["group"] = i+1

    # Concatenate the groups back into a single DataFrame and save the result to a CSV file
    result = pd.concat(groups)
    result.to_csv("new2.csv", index=False)

    return result



# Listening for POST requests to the '/upload' URL
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    no_of_groups = request.form.get('no_of_groups')
    xlsx_file = request.files.get('my-awesome-dropzone')
    print(no_of_groups)
    #final = intoGroup(xlsx_file, no_of_groups)
    #return send_file(final, as_attachment=True)

    return render_template('index.html', result = intoGroup(xlsx_file, no_of_groups))



if __name__ == '__main__':
    app.run(debug=True)