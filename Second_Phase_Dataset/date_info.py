import csv
import re

# Define the path to your text file
file_path = 'answer.txt'

# Categories to extract
categories_to_extract = {'DATE'}

# This will hold the extracted data
extracted_data = []

# Read the text file
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Split the line into components
        parts = line.split('\t')
        if len(parts) > 4 and parts[1] in categories_to_extract:
            # Append a tuple with the category and the corresponding original text and normalized value
            extracted_data.append((parts[1], parts[4], parts[5].strip()))

# Now, let's write the extracted data to a CSV file
output_file = './extracted_date_data.csv'
with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Category', 'Original Text', 'Normalized Value'])
    for data in extracted_data:
        csvwriter.writerow(data)

print(f'Data extracted and saved to {output_file}')