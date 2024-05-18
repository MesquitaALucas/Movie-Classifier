import csv

# Function to parse each line and extract title and year
def parse_line(line):
    parts = line.strip().split('(')
    title = parts[0].strip()
    year = parts[1].replace(')', '').strip()
    return title, year

# Read lines from the text file
with open('films-year.txt', 'r') as file:
    lines = file.readlines()

# Parse each line and store title and year
data = [parse_line(line) for line in lines]

# Write data to CSV file
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Year'])  # Write header
    writer.writerows(data)  # Write data
