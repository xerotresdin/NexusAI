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

# Read and categorize data by quarters and years
with open('2023_dates.txt', 'r') as file:
    dates = [line.strip() for line in file if line.strip()]

date_quarter_year_mapping = {}
for i, date_str in enumerate(dates):
    try:
        # Adjusting to the format MM/DD/YY
        date_obj = datetime.datetime.strptime(date_str, '%m/%d/%y')
        year = date_obj.year
        quarter = get_quarter(date_obj)

        # Map index to quarter and year
        date_quarter_year_mapping[i] = (quarter, year)
    except ValueError:
        print(f"Invalid date format: {date_str}")

# Read other data from files
with open('ID.txt', 'r') as hash_file:
    hash_codes = [line.strip() for line in hash_file if line.strip()]
with open('zip.txt', 'r') as zip_file:
    zip_codes = [line.strip() for line in zip_file if line.strip()]
with open('state.txt', 'r') as state_file:
    states = [line.strip() for line in state_file if line.strip()]
with open('stages.txt', 'r') as stages_file:
    stages = [line.strip() for line in stages_file if line.strip()]

# Process data by quarters and years
data_by_quarter_and_year = defaultdict(lambda: defaultdict(list))

for i, (hash_code, state, zip_code, stage) in enumerate(zip(hash_codes, states, zip_codes, stages)):
    if i in date_quarter_year_mapping:
        quarter, year = date_quarter_year_mapping[i]
        key = (state, zip_code)
        data_by_quarter_and_year[(quarter, year)][key].append({'hash_code': hash_code, 'stage': stage, 'date': dates[i]})

# Save closed-won cases to CSV file
csv_file_path = 'closed_won_cases.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['ID', 'Quarter', 'Date', 'Stage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write closed-won cases
    for (quarter, year), data in data_by_quarter_and_year.items():
        for entries in data.values():
            for entry in entries:
                if entry['stage'] == 'Closed Won':
                    writer.writerow({
                        'ID': entry['hash_code'],
                        'Quarter': f'{quarter} {year}',
                        'Date': entry['date'],
                        'Stage': entry['stage']
                    })

print(f'Closed-won cases saved to {csv_file_path}')
