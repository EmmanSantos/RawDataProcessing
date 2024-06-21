import csv

ave_array =[]
def ave_calc(mode,data = 0):
    
    global ave_array
    data =float(data)

    if (mode == "add"):
        ave_array.append(data)
        return
    elif(mode == "average"):
        
        total = sum(ave_array)
        length = len(ave_array)
       

        ave = total/length
        ave_array = []
        

        return ave

        

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
# file_path = './ValenciaSpain_Kepler_HybridType2XCRR_middlegap0.1_bottomgap0.0233_2024_06_13_1st.csv'
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


wl_counter = 0
for i in range(0,len(data_array)):
    wldiff = abs(float(wl_array[wl_counter][0])-float(data_array[i][1]))
    
    # ldiff = abs(float(data_array[i-1][1])-float(data_array[i][1]))
    # rdiff = abs(float(data_array[i+1][1])-float(data_array[i][1]))
    
    # # print(str(i)," ldiff: ",ldiff)
    # # print(str(i)," rdiff: ",rdiff)
    if(wldiff<0.1):
        # edited_data.append(data_array[i])
        # print(data_array[i][2])
        ave_calc("add",data_array[i][2])
    else:
        wldiff_1 = abs(float(wl_array[wl_counter+1][0])-float(data_array[i][1]))
        if(wldiff_1<0.1):
            
            ave_array.pop(len(ave_array)-1) #remove last point before transition

            ave_power = ave_calc("average")
            edited_data.append([wl_array[wl_counter][0],ave_power])

            ave_calc("add",data_array[i][2])
            wl_counter +=1
        # else:
            # print("Not Appended: ",str(wldiff))




edited_file_path = file_path + "_edited_average_notrans.csv"

with open(edited_file_path, mode='w', newline='') as file:
    csv_writer = csv.writer(file)
    header = ['Wavelength', 'Ave Power']
    csv_writer.writerow(header)

    for row in edited_data:
        csv_writer.writerow(row)