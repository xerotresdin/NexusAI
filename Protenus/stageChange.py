import csv
<<<<<<< HEAD
from collections import defaultdict
import pandas as pd

# Read dates from file
with open('2023_dates.txt', 'r') as date_file:
    dates = [line.strip() for line in date_file if line.strip()]

# Read stages from file
with open('stages.txt', 'r') as stages_file:
    stages = [line.strip() for line in stages_file if line.strip()]

# Combine dates and stages into a defaultdict
data = defaultdict(list)
closed_won_count = 0  # Track the total number of "closed won" cases

for date, stage in zip(dates, stages):
    quarter = pd.to_datetime(date).to_period("Q")
    data[quarter].append({'date': date, 'stage': stage})

    # Check if the case is "closed won"
    if stage == 'Closed Won':
        closed_won_count += 1

# Calculate the total number of entries
total_entries = len(dates)

# Calculate the percentage of total "closed won" cases
closed_won_percentage_total = (closed_won_count / total_entries) * 100

# Calculate the percentage of "closed won" cases for every quarter
quarterly_closed_won_percentages = {}

for quarter, entries in data.items():
    closed_won_count_quarter = sum(entry['stage'] == 'closed won' for entry in entries)
    total_entries_quarter = len(entries)
    closed_won_percentage_quarter = (closed_won_count_quarter / total_entries_quarter) * 100
    quarterly_closed_won_percentages[quarter] = closed_won_percentage_quarter

# Output results
print(f'Total entries: {total_entries}')
print(f'Percentage of total "closed won" cases: {closed_won_percentage_total:.2f}%')

=======
>>>>>>> refs/remotes/origin/main
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

<<<<<<< HEAD
# Output the dates in each quarter by year
for year, quarters in quarters_by_year.items():
    print(f"Year: {year}")
    for quarter, dates in quarters.items():
        print(f"  {quarter}: {dates}")
=======
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
        data_by_quarter_and_year[(quarter, year)][key].append({'hash_code': hash_code, 'stage': stage})

# Calculate and print statistics for each quarter and year
for (quarter, year), data in data_by_quarter_and_year.items():
    total_entries = sum(len(v) for v in data.values())
    unique_entries = len(data)
    duplicate_percentage = ((total_entries - unique_entries) / total_entries) * 100
    # Assuming "Stage 5 - Contracting" as "Closed Won"
    closed_won_count = sum(len([entry for entry in v if entry['stage'] == 'Closed Won']) for v in data.values())
    closed_won_percentage_total = (closed_won_count / total_entries) * 100

    print(f"Year: {year}, Quarter: {quarter}")
    print(f"  Total entries: {total_entries}")
    print(f"  Unique entries: {unique_entries}")
    print(f"  Percentage of duplicate entries: {duplicate_percentage:.2f}%")
    print(f"  Percentage of total 'closed won' cases: {closed_won_percentage_total:.2f}%")
>>>>>>> refs/remotes/origin/main
