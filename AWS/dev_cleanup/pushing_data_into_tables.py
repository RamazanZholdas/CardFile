import xlsxwriter

# Read data from the input file
with open('access_advisor_report.txt', 'r') as f:
    data = f.readlines()

# Create a new Excel file and add a worksheet
workbook = xlsxwriter.Workbook('output.xlsx')
worksheet = workbook.add_worksheet()

# Write the column headers
worksheet.write(0, 0, 'Username')
worksheet.write(0, 1, 'Services not used for 365 days')
worksheet.write(0, 2, 'Services never used')

# Keep track of the current row
row = 1

# Iterate through the data
for line in data:
    # Split the line into words
    words = line.split()

    # Get the username
    username = words[-1].rstrip('.')

    # Check if the service was never used or not used for 180 days
    if 'never' in line:
        service = ' '.join(words[2:words.index('was')])
        worksheet.write(row, 0, username)
        worksheet.write(row, 2, service)
    else:
        service = ' '.join(words[2:words.index('was')])
        worksheet.write(row, 0, username)
        worksheet.write(row, 1, service)

    row += 1

# Close the workbook
workbook.close()