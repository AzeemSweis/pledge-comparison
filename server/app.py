from flask import Flask, request
from flask_cors import CORS
import csv
import io

app = Flask(__name__)
CORS(app)

import csv
import io

def read_csv(file_obj):
    if not isinstance(file_obj, io.StringIO):
        file_obj = io.StringIO(file_obj.read().decode('utf-8'))
    
    reader = csv.reader(file_obj)
    
    # Skip the first 5 rows of irrelevant data
    for _ in range(5):
        next(reader, None)
    
    # Read the headers from row 6
    headers = next(reader, None)
    if headers is None:
        return {}
    
    # Identify the columns for names and amounts
    try:
        name_col_index = headers.index('Name')
        amount_col_index = headers.index('Amount')
    except ValueError:
        return {}  # Proper headers not found

    # Read and process the relevant data rows
    data = {}
    for row in reader:
        # Assuming that the final 4 rows are irrelevant
        if len(row) > max(name_col_index, amount_col_index):
            try:
                name = row[name_col_index].strip()
                amount = float(row[amount_col_index])
                data[name] = amount
            except ValueError:
                continue  # Skip rows where conversion to float fails or irrelevant rows

    return data



def process_files(previous_month_file, current_month_file):
    previous_month = read_csv(previous_month_file)
    current_month = read_csv(current_month_file)

    results = []

    # Check for new entries and changes in the amount
    for name, amount in current_month.items():
        if name not in previous_month:
            results.append(f"New pledge: {name} with amount {amount}")
        elif previous_month[name] != amount:
            results.append(f"Updated pledge for {name}: New amount {amount}")

    # Check for deleted entries
    for name in previous_month:
        if name not in current_month:
            results.append(f"Delete pledge for {name}")

    return "\n".join(results)

@app.route('/upload', methods=['POST'])
def upload_files():
    previous_month_file = request.files['previous_month']
    current_month_file = request.files['current_month']

    previous_month_data = io.StringIO(previous_month_file.read().decode('utf-8'))
    current_month_data = io.StringIO(current_month_file.read().decode('utf-8'))

    results = process_files(previous_month_data, current_month_data)
    
    return {"results": results}

if __name__ == '__main__':
    app.run(debug=True)
