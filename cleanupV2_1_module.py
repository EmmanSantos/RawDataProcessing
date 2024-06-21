import csv


def cleanup(name,csv_path,output_path):
    wl_array = ['1527.60 ', '1527.99 ', '1528.38 ', '1528.77 ', '1529.16 ', '1529.55 ', '1529.94 ', '1530.33 ', '1530.72 ', '1531.12 ', '1531.51 ', '1531.90 ', '1532.29 ', '1532.68 ', '1533.07 ', '1533.47 ', '1533.86 ', '1534.25 ', '1534.64 ', '1535.04 ', '1535.43 ', '1535.82 ', '1536.22 ', '1536.61 ', '1537.00 ', '1537.40 ', '1537.79 ', '1538.19 ', '1538.58 ', '1538.98 ', '1539.37 ', '1539.77 ', '1540.16 ', '1540.56 ', '1540.95 ', '1541.35 ', '1541.75 ', '1542.14 ', '1542.54 ', '1542.94 ', '1543.33 ', '1543.73 ', '1544.13 ', '1544.53 ', '1544.92 ', '1545.32 ', '1545.72 ', '1546.12 ', '1546.52 ', '1546.92 ', '1547.32 ', '1547.72 ', '1548.11 ', '1548.51 ', '1548.91 ', '1549.32 ', '1549.72 ', '1550.12 ', '1550.52 ', '1550.92 ', '1551.32 ', '1551.72 ', '1552.12 ', '1552.52 ', '1552.93 ', '1553.33 ', '1553.73 ', '1554.13 ', '1554.54 ', '1554.94 ', '1555.34 ', '1555.75 ', '1556.15 ', '1556.55 ', '1556.96 ', '1557.36 ', '1557.77 ', '1558.17 ', '1558.58 ', '1558.98 ', '1559.39 ', '1559.79 ', '1560.20 ', '1560.61 ', '1561.01 ', '1561.42 ', '1561.83 ', '1562.23 ', '1562.64 ', '1563.05 ', '1563.45 ', '1563.86 ', '1564.27 ', '1564.68 ', '1565.09 ', '1565.50 ', '1565.90 ', '1566.31 ', '1566.72 ', '1567.13 ']
    # Define the file path to your CSV file
    # file_path = './ValenciaSpain_Kepler_HybridType2XCRR_middlegap0.1_bottomgap0.0133_2024_06_13_1st.csv'
    file_path = csv_path

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
        wldiff = abs(float(wl_array[wl_counter])-float(data_array[i][1])) #diff with current wavelength
        
 
        if(wldiff<0.1):
            edited_data.append(data_array[i])
            # print("Appended: ",str(wldiff))
            # print("Wavelength: ",data_array[i][1])
        else:
            #check if the input has switched to next WL
            wldiff_1 = abs(float(wl_array[wl_counter+1])-float(data_array[i][1])) #diff with next wavelength
            if(wldiff_1<0.1):
                # edited_data.append(data_array[i]) #do not append first point after transition
                if(len(edited_data)>0):
                    edited_data.pop(len(edited_data)-1) #remove last point before transition
                wl_counter +=1
            else:
                #check for earlier runs where WL started at 1529.16
                wl_diff_1529 = abs(float(wl_array[4])-float(data_array[i][1]))
                if wl_diff_1529 < 0.1:
                    wl_counter = 4
                # print("Not Appended: ",str(wldiff))




    edited_file_path = output_path +"/"+ name + "_edited_removedtransition.csv"

    with open(edited_file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        header = ['Time', 'Wavelength', 'Power']
        csv_writer.writerow(header)

        for row in edited_data:
            csv_writer.writerow(row)
    
    return edited_data