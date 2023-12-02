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

# Combine hash codes, states, and zip codes into a defaultdict
data = defaultdict(list)
for hash_code, state, zip_code in zip(hash_codes, states, zip_codes):
    key = (state, zip_code)
    data[key].append(hash_code)

# Calculate the percentage of duplicate zip codes and states
total_entries = len(hash_codes)
unique_entries = len(data)
duplicate_percentage = ((total_entries - unique_entries) / total_entries) * 100

print(f'Total entries: {total_entries}')
print(f'Unique entries: {unique_entries}')
print(f'Percentage of duplicate entries: {duplicate_percentage:.2f}%')

# Save grouped data to CSV file
csv_file_path = 'grouped_dataset.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['state', 'zipcode', 'hash_codes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()

    # Write grouped data
    for (state, zipcode), hash_codes_list in data.items():
        writer.writerow({'state': state, 'zipcode': zipcode, 'hash_codes': ', '.join(hash_codes_list)})

print(f'Grouped dataset saved to {csv_file_path}')
