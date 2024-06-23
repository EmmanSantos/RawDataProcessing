import csv
from math import log10
ave_array = []

# takes in arbitrary wavelength returns closest wavelength if difference with possible value is less than 0.05nm
def wl_select(wl_in):
    wl_array = ['1527.60 ', '1527.99 ', '1528.38 ', '1528.77 ', '1529.16 ', '1529.55 ', '1529.94 ', '1530.33 ', '1530.72 ', '1531.12 ', '1531.51 ', '1531.90 ', '1532.29 ', '1532.68 ', '1533.07 ', '1533.47 ', '1533.86 ', '1534.25 ', '1534.64 ', '1535.04 ', '1535.43 ', '1535.82 ', '1536.22 ', '1536.61 ', '1537.00 ', '1537.40 ', '1537.79 ', '1538.19 ', '1538.58 ', '1538.98 ', '1539.37 ', '1539.77 ', '1540.16 ', '1540.56 ', '1540.95 ', '1541.35 ', '1541.75 ', '1542.14 ', '1542.54 ', '1542.94 ', '1543.33 ', '1543.73 ', '1544.13 ', '1544.53 ', '1544.92 ', '1545.32 ', '1545.72 ', '1546.12 ', '1546.52 ', '1546.92 ', '1547.32 ', '1547.72 ', '1548.11 ', '1548.51 ', '1548.91 ', '1549.32 ', '1549.72 ', '1550.12 ', '1550.52 ', '1550.92 ', '1551.32 ', '1551.72 ', '1552.12 ', '1552.52 ', '1552.93 ', '1553.33 ', '1553.73 ', '1554.13 ', '1554.54 ', '1554.94 ', '1555.34 ', '1555.75 ', '1556.15 ', '1556.55 ', '1556.96 ', '1557.36 ', '1557.77 ', '1558.17 ', '1558.58 ', '1558.98 ', '1559.39 ', '1559.79 ', '1560.20 ', '1560.61 ', '1561.01 ', '1561.42 ', '1561.83 ', '1562.23 ', '1562.64 ', '1563.05 ', '1563.45 ', '1563.86 ', '1564.27 ', '1564.68 ', '1565.09 ', '1565.50 ', '1565.90 ', '1566.31 ', '1566.72 ', '1567.13 ']
    
    for i in range(0,len(wl_array)):
        wl_diff =abs(float(wl_array[i])-wl_in)
        # print(wl_diff)
        if (wl_diff)<0.05:
            return float(wl_array[i])
    return False #no wavelength found

#calculates average per wavelength
# add mode: appends data to array
# average mode: returns the average and clears the value of ave_array
def ave_calc(mode,data = 0):
    
    global ave_array
    mw_array = []

    data =float(data)

    if (mode == "add"):
        ave_array.append(data)

        return
    elif(mode == "average"):

        for a in ave_array:
            mw_array.append(10**(a/10))
        
        total = sum(mw_array)
        length = len(mw_array)
        ave_mw = total/length
        
        ave = 10*log10(ave_mw)

        ave_array = []
        

        return ave


def cleanup(name,csv_path,output_path):
    global ave_array
    
    file_path = csv_path

    # Empty array where .csv data will be stored to
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

    # array for storing the cleaned data
    edited_data = []

    #array for storing the averaged data
    ave_data = []
    
   
    # ALGO OVERVIEW

    # Assumptions:
    #  - The laser is already stable at the first sample
    #  - Algorithm assumes that wavlength sweep is increasing
    #  - if the input data has 1567.13 as the wavelenght at the start, the algo deletes this until it finds a lower wavelength
    #     - this assumption is because the user may have not reset the wavelenth to 1527.6 or a lower value before starting a sweep
     
    # Variables
    #  - curr_wl is the wavelength that the algorithm is comparing to
    #  - prev_wl is the previous wavelength
    #  - curr_wl and prev_wl may take on any of the possible values that the laser can output
     
    #  FLOW
    #   - wl_select is called to determine if the measured WL is close enough to one of the expected values and the value is stored to curr_wl
    #   - if curr_wl is not False, the current row of the unprocessed data is stored to the edited_array and prev_wl is updated
    #   - the current measured wavelength is appened to ave_array
    #   - if curr_wl is False, this means that there was no wavelength match found and the current row of the unprocessed data is skipped
      
    #   Wavelength change
    #   - this occurs when curr_wl is not false but curr_wl is not equal to prev_wl
    #   - when this is detected, the last element of cleaned_array is deleted
    #     - it has been observed that before the laser switches wavelength the power at the current wavelength drops
    #     - thus the last sample before switching wavelengths is deleted by the algo
    #   - ave_calc is called to average the current values of ave_array
    #     - the curr_wl and average result is appened to ave_data
    # 
    
    curr_wl = wl_select(float(data_array[0][1]))
    prev_wl = curr_wl
   

    for i in range(0,len(data_array)):
        curr_wl = wl_select(float(data_array[i][1]))
        # wldiff = abs(float(wl_array[wl_counter])-float(data_array[i][1])) #diff with current wavelength
        
 
        if(curr_wl):
            if(prev_wl == curr_wl):
                edited_data.append(data_array[i])
                ave_calc("add",data_array[i][2])
                prev_wl = curr_wl
                # print("Wavelength: ",data_array[i][1])
                if(i == len(data_array)-1):
                    ave_power = ave_calc("average")
                    ave_data.append([prev_wl,ave_power]) 
                
                
            else:
                
                if (curr_wl-prev_wl)<0.6 and (curr_wl-prev_wl)>0: # means that wavelength change is according to behavior of sweep
                    
                    # print(prev_wl)
                    # print(curr_wl)  
                    if(len(edited_data)>0 and len(ave_array)>0):
                        edited_data.pop(len(edited_data)-1) #remove last point before transition and not append current point
                        ave_power = ave_calc("average")
                        ave_data.append([prev_wl,ave_power])
                        prev_wl = curr_wl

                elif prev_wl == 1567.13: #sweep was not reset from 1567.13
                    edited_data =[]
                    ave_calc("average")
                    ave_data = []
                    edited_data.append(data_array[i])
                    prev_wl = curr_wl
                
                
        





    edited_file_path = output_path +"/"+ name + "_edited_removedtransition.csv"

    with open(edited_file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        header = ['Time', 'Wavelength', 'Power']
        csv_writer.writerow(header)

        for row in edited_data:
            csv_writer.writerow(row)

    return [edited_data,ave_data]