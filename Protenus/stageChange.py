import csv
from collections import defaultdict

# Read hash codes from file
with open('ID.txt', 'r') as hash_file:
    hash_codes = [line.strip() for line in hash_file if line.strip()]

# Read zip codes from file
with open('zip.txt', 'r') as zip_file:
    zip_codes = [line.strip() for line in zip_file if line.strip()]

# Read states from file
with open('state.txt', 'r') as state_file:
    states = [line.strip() for line in state_file if line.strip()]

# Read stages from file
with open('stages.txt', 'r') as stages_file:
    stages = [line.strip() for line in stages_file if line.strip()]

# Combine hash codes, states, zip codes, and stages into a defaultdict
data = defaultdict(list)
closed_won_count = 0  # Track the total number of "closed won" cases

for hash_code, state, zip_code, stage in zip(hash_codes, states, zip_codes, stages):
    key = (state, zip_code)
    data[key].append({'hash_code': hash_code, 'stage': stage})
    
    # Check if the case is "closed won"
    if stage == 'Closed Won':
        closed_won_count += 1

# Calculate the percentage of duplicate zip codes and states
total_entries = len(hash_codes)
unique_entries = len(data)
duplicate_percentage = ((total_entries - unique_entries) / total_entries) * 100

# Calculate the percentage of total "closed won" cases
closed_won_percentage_total = (closed_won_count / total_entries) * 100

print(f'Total entries: {total_entries}')
print(f'Unique entries: {unique_entries}')
print(f'Percentage of duplicate entries: {duplicate_percentage:.2f}%')
print(f'Percentage of total "closed won" cases: {closed_won_percentage_total:.2f}%')

import datetime

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

# Read dates from file
with open('2023_dates.txt', 'r') as file:
    dates = [line.strip() for line in file if line.strip()]

# Separate dates into quarters by year
quarters_by_year = {}
for date_str in dates:
    try:
        # Adjusting to the format MM/DD/YY
        date_obj = datetime.datetime.strptime(date_str, '%m/%d/%y')
        year = date_obj.year
        quarter = get_quarter(date_obj)

        # Initialize the year and quarter if not already done
        if year not in quarters_by_year:
            quarters_by_year[year] = {'Q1': [], 'Q2': [], 'Q3': [], 'Q4': []}

        # Append the date to the appropriate quarter and year
        quarters_by_year[year][quarter].append(date_str)
    except ValueError:
        print(f"Invalid date format: {date_str}")

# Output the dates in each quarter by year
for year, quarters in quarters_by_year.items():
    print(f"Year: {year}")
    for quarter, dates in quarters.items():
        print(f"  {quarter}: {dates}")
