import pandas as pd
import re
from datetime import datetime, timedelta

# Sample data setup
parts_data = {
    'Part': ['Battery', 'Oil Filter', 'Brake Pads', 'Tires', 'Air Filter'],
    'Lifespan_Months': [36, 6, 24, 48, 12],  # Lifespan in months
    'Installation_Date': ['2021-01-15', '2023-04-10', '2022-08-20', '2021-06-01', '2023-02-25']
}

# Convert parts data into a DataFrame and parse dates
parts_df = pd.DataFrame(parts_data)
parts_df['Installation_Date'] = pd.to_datetime(parts_df['Installation_Date'])

# User input data
usage_data = {}

# Collect user inputs
usage_data['Total_Mileage'] = float(input("Enter the total mileage of the car (in km): "))
usage_data['Average_Speed'] = float(input("Enter the average speed of the car (in km/h): "))
usage_data['Environment_Notes'] = input("Enter any environmental conditions (comma-separated): ").split(',')
usage_data['Maintenance_Logs'] = []
while True:
    log = input("Enter a maintenance log entry (or type 'done' to finish): ")
    if log.lower() == 'done':
        break
    usage_data['Maintenance_Logs'].append(log)

# 1. Maintenance Log Analysis
def analyze_log(log):
    critical_terms = ['noise', 'wear', 'vibration', 'fail']
    log = log.lower()
    if any(term in log for term in critical_terms):
        return 'Potential Issue Detected'
    return 'No Issue Detected'

# Analyze each maintenance log entry
logs_analysis = [analyze_log(log) for log in usage_data['Maintenance_Logs']]
usage_data['Log_Analysis'] = logs_analysis

# 2. Usage and Mileage Tracking
def mileage_based_alert(total_mileage):
    # Define thresholds for alerts based on mileage for parts
    if total_mileage > 15000:
        return 'Alert: Oil Change Needed'
    elif total_mileage > 30000:
        return 'Alert: Brake Pads Replacement'
    else:
        return 'No Immediate Maintenance Needed'

usage_alert = mileage_based_alert(usage_data['Total_Mileage'])

# 3. Vehicle Age and Parts Lifespan Estimates
def check_lifespan(row):
    install_date = row['Installation_Date']
    lifespan = row['Lifespan_Months']
    expiration_date = install_date + timedelta(days=lifespan * 30)
    if datetime.now() >= expiration_date:
        return 'Maintenance Due'
    else:
        return 'No Maintenance Needed'

parts_df['Maintenance_Status'] = parts_df.apply(check_lifespan, axis=1)

# 4. Environmental Condition Monitoring
def environment_check(conditions):
    warning_conditions = ['rough terrain', 'rain', 'extreme heat']
    for note in conditions:
        if any(condition in note.lower() for condition in warning_conditions):
            return 'Preventive Maintenance Suggested'
    return 'No Preventive Maintenance Needed'

environment_alert = environment_check(usage_data['Environment_Notes'])

# Display Results
print("\nMaintenance Log Analysis:")
for log, result in zip(usage_data['Maintenance_Logs'], usage_data['Log_Analysis']):
    print(f"Log: {log} => {result}")

print("\nUsage and Mileage Tracking Alert:")
print(usage_alert)

print("\nVehicle Parts Lifespan Maintenance Status:")
print(parts_df[['Part', 'Installation_Date', 'Lifespan_Months', 'Maintenance_Status']])

print("\nEnvironmental Condition Monitoring Alert:")
print(environment_alert)
