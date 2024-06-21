import csv

wl_array = []
wl_file_path = './wavelengths.csv'
with open(wl_file_path, mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # Append each row to the data_array
        wl_array.append(row)
print(wl_array)

# Define the file path to your CSV file
# file_path = './ValenciaSpain_Kepler_HybridType2XCRR_middlegap0.1_bottomgap0.0133_2024_06_13_1st.csv'
file_path = 'ValenciaSpain_Kepler_HybridType2XCRR_middlegap0.1_bottomgap0.02_2024_06_13_1st.csv'

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

wl_counter = 0
for i in range(0,len(data_array)):
    wldiff = abs(float(wl_array[wl_counter][0])-float(data_array[i][1])) #diff with current wavelength
    
    # ldiff = abs(float(data_array[i-1][1])-float(data_array[i][1]))
    # rdiff = abs(float(data_array[i+1][1])-float(data_array[i][1]))
    
    # # print(str(i)," ldiff: ",ldiff)
    # # print(str(i)," rdiff: ",rdiff)
    if(wldiff<0.1):
        edited_data.append(data_array[i])
    else:
        wldiff_1 = abs(float(wl_array[wl_counter+1][0])-float(data_array[i][1])) #diff with next wavelength
        if(wldiff_1<0.1):
            # edited_data.append(data_array[i]) #do not append first point after transition
            edited_data.pop(len(edited_data)-1) #remove last point before transition
            wl_counter +=1
        else:
            print("Not Appended: ",str(wldiff))




edited_file_path = file_path + "_edited_removedtransition.csv"

with open(edited_file_path, mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    header = ['Time', 'Wavelength', 'Power']
    csv_writer.writerow(header)

    for row in edited_data:
        csv_writer.writerow(row)