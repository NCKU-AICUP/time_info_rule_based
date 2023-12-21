import csv
import re


# Load the data from the TXT file
input_file = 'answer.txt'  # Replace with the path to your answer.txt file
extracted_data = []

with open(input_file, 'r', encoding='utf-8') as txtfile:
    for line in txtfile:
        # Split each line into columns
        columns = line.strip().split('\t')  # Assuming tab-separated values

        # Check if the second column is one of the desired categories
        if columns[1] in ["TIME", "DATE", "SET", "DURATION"]:
            # Append the relevant columns (Category, Original Text, Normalized Value)
            extracted_data.append((columns[1], columns[4], columns[5]))

# Now, write the extracted data to a CSV file
output_file = 'extracted_data.csv'  # Replace with your desired output file path
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write header
    csvwriter.writerow(['Category', 'Original Text', 'Normalized Value'])
    # Write data
    for data in extracted_data:
        csvwriter.writerow(data)
