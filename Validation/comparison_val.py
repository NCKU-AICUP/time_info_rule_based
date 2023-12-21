import pandas as pd

# Load the processed data from your CSV file
file_path = './processed_data_val.csv'  # Replace with the path to your CSV file
processed_data = pd.read_csv(file_path)

# Compare 'Normalized Value' and 'Normalized Value Corrected' columns
comparison_result = processed_data['Normalized Value'].astype(str) == processed_data['Normalized Value Corrected'].astype(str)

# Display a summary of the comparison
comparison_summary = comparison_result.value_counts()
print(comparison_summary)


# Extract rows where 'Normalized Value' and 'Normalized Value Corrected' do not match
mismatched_data = processed_data[processed_data['Normalized Value'].astype(str) != processed_data['Normalized Value Corrected'].astype(str)]

# Save the mismatched data to a new CSV file
mismatched_file_path = 'mismatched_data_val.csv'  # Replace with your desired file path
mismatched_data.to_csv(mismatched_file_path, index=False)
