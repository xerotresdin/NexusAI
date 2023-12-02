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

print("\nClosed Won Percentages for Each Quarter:")
for quarter, percentage in quarterly_closed_won_percentages.items():
    print(f'{quarter}: {percentage:.2f}%')
