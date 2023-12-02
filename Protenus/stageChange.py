import csv
import datetime
from collections import defaultdict

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

def predict_future_revenue(quarterly_revenue, future_quarters):
    growth_rates = []
    sorted_quarters = sorted(quarterly_revenue.keys())
    for i in range(1, len(sorted_quarters)):
        previous_revenue = quarterly_revenue[sorted_quarters[i - 1]]
        current_revenue = quarterly_revenue[sorted_quarters[i]]
        if previous_revenue > 0:
            growth_rate = (current_revenue - previous_revenue) / previous_revenue
            growth_rates.append(growth_rate)

    if not growth_rates:
        return "Insufficient data for prediction"

    average_growth_rate = sum(growth_rates) / len(growth_rates)
    last_known_revenue = quarterly_revenue[sorted_quarters[-1]]
    predictions = {}
    for quarter in future_quarters:
        predicted_revenue = last_known_revenue * (1 + average_growth_rate)
        predictions[quarter] = predicted_revenue
        last_known_revenue = predicted_revenue

    return predictions

hospital_first_contact = {}
duration_data = {
    'existing_diversion': [],
    'existing_privacy': [],
    'new_diversion': [],
    'new_privacy': []
}
quarterly_revenue = defaultdict(float)

with open('2023_dates.txt', 'r') as file:
    dates = [line.strip() for line in file if line.strip()]

date_quarter_year_mapping = {}
for i, date_str in enumerate(dates):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%m/%d/%Y')
        year = date_obj.year
        quarter = get_quarter(date_obj)
        date_quarter_year_mapping[i] = (quarter, year)
    except ValueError:
        print(f"Invalid date format: {date_str}")

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

annual_amounts = []
with open('opportunity_annual_amount.txt', 'r') as amount_file:
    for i, line in enumerate(amount_file):
        try:
            amount = float(line.strip()) if line.strip() else None
        except ValueError:
            print(f"Invalid amount format: '{line.strip()}' at line {i+1}")
            amount = None
        annual_amounts.append(amount)

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

        if hash_code not in hospital_first_contact or current_date < hospital_first_contact[hash_code]:
            hospital_first_contact[hash_code] = current_date

        data_by_quarter_and_year[(quarter, year)][key].append({
            'hash_code': hash_code,
            'stage': stage,
            'date': date_str,
            'customer_type': customer_type,
            'product_type': product_type,
            'annual_amount': annual_amounts[i] if i < len(annual_amounts) else None
        })

csv_file_path = 'closed_won_cases.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['ID', 'Quarter', 'Date', 'Stage', 'Customer_Type', 'Product_Type', 'First_Contact_Date', 'Duration_Months', 'Annual_Amount']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for (quarter, year), data in data_by_quarter_and_year.items():
        for entries in data.values():
            for entry in entries:
                if entry['stage'] == 'Closed Won':
                    end_date = datetime.datetime.strptime(entry['date'], '%m/%d/%Y')
                    start_date = hospital_first_contact[entry['hash_code']]
                    duration_days = (end_date - start_date).days
                    duration_months = duration_days // 30

                    category_key = f"{entry['customer_type'].lower()}_{entry['product_type'].lower()}"
                    if category_key in duration_data:
                        duration_data[category_key].append(duration_months)

                    annual_amount = entry['annual_amount']
                    if annual_amount is not None:
                        quarterly_key = f"{year} {quarter}"
                        quarterly_revenue[quarterly_key] += annual_amount

                    writer.writerow({
                        'ID': entry['hash_code'],
                        'Quarter': f'{quarter} {year}',
                        'Date': entry['date'],
                        'Stage': entry['stage'],
                        'Customer_Type': entry['customer_type'],
                        'Product_Type': entry['product_type'],
                        'First_Contact_Date': start_date.strftime('%m/%d/%Y'),
                        'Duration_Months': duration_months,
                        'Annual_Amount': annual_amount if annual_amount is not None else "N/A"
                    })

average_durations = {category: (sum(durations) / len(durations) if durations else 0) for category, durations in duration_data.items()}
for category, avg_duration in average_durations.items():
    print(f"Average duration for {category}: {avg_duration:.2f} months")

future_quarters = ["Q3 2023", "Q4 2023"]
future_revenue_predictions = predict_future_revenue(quarterly_revenue, future_quarters)

for quarter, revenue in future_revenue_predictions.items():
    print(f"Predicted revenue for {quarter}: ${revenue:.2f}")
