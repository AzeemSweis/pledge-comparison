from flask import Flask, request
from flask_cors import CORS
import csv
import io

app = Flask(__name__)
CORS(app)

def read_csv(file_obj):
    # Convert file storage to StringIO for csv reader compatibility if not already a StringIO
    if not isinstance(file_obj, io.StringIO):
        file_obj = io.StringIO(file_obj.read().decode('utf-8'))
    reader = csv.reader(file_obj)
    # Skip the header if present
    next(reader, None)
    return {rows[0]: float(rows[1]) for rows in reader if len(rows) >= 2 and rows[1].replace('.', '', 1).isdigit()}

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
