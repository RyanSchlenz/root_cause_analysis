import pandas as pd

# Define the paths for the input and output CSV files
input_csv_file_path = 'filtered_subjects.csv'  # Update this path
output_csv_file_path = 'aggregated_data.csv'  # Update this path

# Load the CSV file into a DataFrame
df = pd.read_csv(input_csv_file_path)

# Print unique values in the 'Product - Service Desk Tool' column
print("Unique 'Product - Service Desk Tool' values:")
print(df['Product - Service Desk Tool'].unique())

# Ensure relevant columns are treated as strings and handle possible NaN values
df['Product - Service Desk Tool'] = df['Product - Service Desk Tool'].astype(str).replace('nan', '').str.strip()
df['Ticket created - Day of month'] = df['Ticket created - Day of month'].astype(float).fillna(0).astype(int)
df['Ticket created - Month'] = df['Ticket created - Month'].astype(str).str.strip()

# Combine 'Ticket created - Day of month' and 'Ticket created - Month' into a single 'Date' column
df['Date'] = df.apply(lambda row: f"{row['Ticket created - Month']}/{int(row['Ticket created - Day of month']):02d}", axis=1)

# Replace month names with numerical values for proper datetime conversion
month_mapping = {
    'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
    'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
}
df['Date'] = df['Date'].replace(month_mapping, regex=True)

# Convert the 'Date' column to a datetime format for proper grouping, ignoring the year
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d', errors='coerce')

# Drop rows where 'Date' is NaT (Not a Time) after conversion
df = df.dropna(subset=['Date'])

# Ensure the 'Date' column is in the desired format for output
df['Date'] = df['Date'].dt.strftime('%m/%d')

# Define a mapping for category combinations
category_mapping = {
    'Mobile Device': 'MOBI',
    'Azure': 'Azure Virtual Desktop (AVD)',
    'Outlook': 'Exchange',
    'Fax': 'Faxage',
    'Hardware': 'Equipment/Hardware',
    'Equipment': 'Equipment/Hardware',
    'No Touch Device (NTD)': 'Equipment/Hardware',
    'FedEx': 'Equipment/Hardware',
    'Laptop Troubleshooting': 'Equipment/Hardware',
    'Equipment Order': 'Equipment/Hardware',
    'BitLocker': 'Equipment/Hardware',
    'Internet Account': 'Network',
    'Service Provider': 'Network',
    'WiFi Connection': 'Network',
    'No Response - Requester': 'End User Training',
    'Unknown End User': 'End User Training',
    'Voicemail': 'End User Training',
    'Citrix': 'Azure Virtual Desktop (AVD)',
    'J-Drive': 'Drive Access',
    'H-Drive': 'Drive Access',
    'G-Drive': 'Drive Access',
    'Microsoft Edge': 'Microsoft 365 Products',
    'Windows': 'Microsoft 365 Products',
    'Teams': 'Microsoft 365 Products',
    'Other (please list below)': 'Other',
    'Google Chrome': 'Other',
    'Fuze': 'Fuze/8x8',
    'Microsoft Office 365 Tools': 'Microsoft 365 Products',
    'Pennant University': 'Pennant/Hartford Guide',
    'PointCare': 'HCHB',
    'Provider Link': 'HCHB',
    'SPAM': 'Other',
    'Verizon': 'MOBI',
    'Smartsheets': 'Smartsheet',
    'Automation Mobile Device Hire': 'UAP',
    'Automation Mobile Device Term': 'UAP',
    'Tiger Connect': 'MOBI',
    'Welcome Home': 'PCC',
    'Pennant Guide': 'Pennant/Hartford Guide',
    'ADUC': 'ADUC'  # Ensure ADUC is explicitly mapped
}

# Apply category mapping, keeping unmapped values assigned to 'Other'
df['Product - Service Desk Tool'] = df['Product - Service Desk Tool'].replace(category_mapping)
print("Mapped 'Product - Service Desk Tool' values:")
print(df['Product - Service Desk Tool'].unique())  # Check the unique values after mapping

df.loc[~df['Product - Service Desk Tool'].isin(category_mapping.values()), 'Product - Service Desk Tool'] = 'Other'

# Ensure 'Tickets' column exists. If not, add a placeholder column with 1 for counting
if 'Tickets' not in df.columns:
    df['Tickets'] = 1  # Assign 1 to each row, so each row counts as 1 ticket

# Group by 'Date' and 'Product - Service Desk Tool' and aggregate the ticket counts
aggregated_df = df.groupby(['Date', 'Product - Service Desk Tool']).agg({'Tickets': 'sum'}).reset_index()
print("Aggregated data:")
print(aggregated_df)  # Check the aggregated data

# Rename 'Tickets' column to 'Ticket Count'
aggregated_df.rename(columns={'Tickets': 'Ticket Count'}, inplace=True)

# Initialize an empty list to hold the new rows including the totals and blank rows
final_rows = []

# Filter and print "Other" categories separately
other_df = df[df['Product - Service Desk Tool'] == 'Other']

# Print the uncategorized "Other" items
print("Other categories (not mapped):")
print(other_df[['Date', 'Product - Service Desk Tool', 'Tickets']])

# Iterate over each date group to calculate totals and add rows
for date, group in aggregated_df.groupby('Date'):
    # Append the grouped data (for each day) to the final rows list
    final_rows.append(group)
    
    # Calculate the total ticket count for that date
    total_tickets = group['Ticket Count'].sum()
    
    # Create a total row with a 'Total' in the Product - Service Desk Tool column
    total_row = pd.DataFrame({
        'Date': [date],
        'Product - Service Desk Tool': ['Total'],
        'Ticket Count': [total_tickets]
    })
    
    # Append the total row to the final rows
    final_rows.append(total_row)
    
    # Add an empty row (to create a space between each day)
    empty_row = pd.DataFrame({
        'Date': [''],
        'Product - Service Desk Tool': [''],
        'Ticket Count': ['']
    })
    final_rows.append(empty_row)

# Concatenate all the rows back into a single DataFrame
final_df = pd.concat(final_rows, ignore_index=True)

# Save the final DataFrame to a new CSV file
final_df.to_csv(output_csv_file_path, index=False)

# Print all defined categories after mapping
print("Final DataFrame:")
print(final_df)

print(f"Aggregated ticket counts with totals saved to {output_csv_file_path}")
