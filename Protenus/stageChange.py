import csv
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
    if stage == 'closed won':
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

<<<<<<< HEAD
print("\nClosed Won Percentages for Each Quarter:")
for quarter, percentage in quarterly_closed_won_percentages.items():
    print(f'{quarter}: {percentage:.2f}%')
=======
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
>>>>>>> refs/remotes/origin/main
