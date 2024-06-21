import csv

wl_array = []
wl_file_path = './wavelengths.csv'
with open(wl_file_path, mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # Append each row to the data_array
        wl_array.append(row)


# Define the file path to your CSV file
file_path = './ValenciaSpain_Kepler_HybridType2XCRR_middlegap0.1_bottomgap0.0133_2024_06_13_1st.csv'

# Initialize an empty list to store the data
data_array = []

# Open the CSV file
with open(file_path, mode='r', newline='') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    
    # Skip the first line (header)
    next(csv_reader)
    
    # Iterate over the remaining lines in the CSV file
    for row in csv_reader:
        # Append each row to the data_array
        data_array.append(row)

# Print the resulting array
# for row in data_array:
#     print(row)

edited_data = []
edited_data.append(data_array[1])


for i in range(1,len(data_array)-1):
    ldiff = abs(float(data_array[i-1][1])-float(data_array[i][1]))
    rdiff = abs(float(data_array[i+1][1])-float(data_array[i][1]))
    
    # print(str(i)," ldiff: ",ldiff)
    # print(str(i)," rdiff: ",rdiff)

    if ldiff < .1 and rdiff < .1:
        edited_data.append(data_array[i])
    # else:
    #     print("Not Appended")

# for row in edited_data:
#     print(row)

edited_file_path = file_path + "_edited.csv"

with open(edited_file_path, mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    header = ['Time', 'Wavelength', 'Power']
    csv_writer.writerow(header)

    for row in edited_data:
        csv_writer.writerow(row)