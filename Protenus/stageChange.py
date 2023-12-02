import csv
import datetime
from collections import defaultdict

# Function to determine the quarter of a date
def get_quarter(date):
    month = date.month
    if 1 <= month <= 3:
        return 'Q1'
    elif 4 <= month <= 6:
        return 'Q2'
    elif 7 <= month <= 9:
        return 'Q3'
    else:
        return 'Q4'

# Initialize hospital_first_contact dictionary
hospital_first_contact = {}

# Read and categorize data by quarters and years
with open('2023_dates.txt', 'r') as file:
    dates = [line.strip() for line in file if line.strip()]

date_quarter_year_mapping = {}
for i, date_str in enumerate(dates):
    try:
        # Adjusting to the format MM/DD/YYYY
        date_obj = datetime.datetime.strptime(date_str, '%m/%d/%Y')
        year = date_obj.year
        quarter = get_quarter(date_obj)

        # Map index to quarter and year
        date_quarter_year_mapping[i] = (quarter, year)
    except ValueError:
        print(f"Invalid date format: {date_str}")

# Improved date parsing with error reporting
for i, date_str in enumerate(dates):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%m/%d/%Y')
        year = date_obj.year
        quarter = get_quarter(date_obj)
        date_quarter_year_mapping[i] = (quarter, year)
    except ValueError:
        print(f"Error parsing date: '{date_str}' at line {i+1}")

# Read other data from files
with open('ID.txt', 'r') as hash_file:
    hash_codes = [line.strip() for line in hash_file if line.strip()]
with open('zip.txt', 'r') as zip_file:
    zip_codes = [line.strip() for line in zip_file if line.strip()]
with open('state.txt', 'r') as state_file:
    states = [line.strip() for line in state_file if line.strip()]
with open('stages.txt', 'r') as stages_file:
    stages = [line.strip() for line in stages_file if line.strip()]
with open('history.txt', 'r') as history_file:
    customer_types = [line.strip() for line in history_file if line.strip()]
with open('product.txt', 'r') as product_file:
    product_types = [line.strip() for line in product_file if line.strip()]

# Process data by quarters and years
data_by_quarter_and_year = defaultdict(lambda: defaultdict(list))

for i, (hash_code, state, zip_code, stage, customer_type, product_type, date_str) in enumerate(zip(hash_codes, states, zip_codes, stages, customer_types, product_types, dates)):
    try:
        current_date = datetime.datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        print(f"Invalid date format: {date_str}")
        continue

    if i in date_quarter_year_mapping:
        quarter, year = date_quarter_year_mapping[i]
        key = (state, zip_code)
        
        # Update the hospital's first point of contact date if it's older than the current record
        if hash_code not in hospital_first_contact or current_date < hospital_first_contact[hash_code]:
            hospital_first_contact[hash_code] = current_date

        data_by_quarter_and_year[(quarter, year)][key].append({
            'hash_code': hash_code,
            'stage': stage,
            'date': date_str,
            'customer_type': customer_type,
            'product_type': product_type
        })

# Save closed-won cases to CSV file
csv_file_path = 'closed_won_cases.csv'

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['ID', 'Quarter', 'Date', 'Stage', 'Customer_Type', 'Product_Type', 'First_Contact_Date', 'Duration_Months']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Process and write closed-won cases
    for (quarter, year), data in data_by_quarter_and_year.items():
        for entries in data.values():
            for entry in entries:
                if entry['stage'] == 'Closed Won':
                    # Calculate the duration in months more accurately
                    end_date = datetime.datetime.strptime(entry['date'], '%m/%d/%Y')
                    start_date = hospital_first_contact[entry['hash_code']]

                    # Calculate full years and months difference
                    year_diff = end_date.year - start_date.year
                    month_diff = end_date.month - start_date.month

                    # Adjust if start date day is greater than end date day
                    day_adjustment = 1 if start_date.day > end_date.day else 0

                    # Final duration in months
                    duration_months = year_diff * 12 + month_diff - day_adjustment

                    writer.writerow({
                        'ID': entry['hash_code'],
                        'Quarter': f'{quarter} {year}',
                        'Date': entry['date'],
                        'Stage': entry['stage'],
                        'Customer_Type': entry['customer_type'],
                        'Product_Type': entry['product_type'],
                        'First_Contact_Date': start_date.strftime('%m/%d/%Y'),
                        'Duration_Months': duration_months
                    })

print(f'Closed-won cases saved to {csv_file_path}')
