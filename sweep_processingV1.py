import os
# import cleanupV2_1_module
import cleanupV2_2_unorderedWL
import matplotlib.pyplot as plt
import numpy as np
import pybaselines

def logtomw(input_array):
    for i in range(0,len(input_array)):
        input_array[i]=10**(input_array[i]/10)

    return input_array

#create directories
csv_dir = input("Enter the folder name of the raw CSV (folder must be in same folder as exe): ")

# csv_dir = "./unprocessedUpdate"
processed_dir = './'+csv_dir+"-PROCESSED_baseline"
graph_dir = processed_dir
baseline_dir = processed_dir+"/baseline_corr/dBm"
baseline_dir_mw = processed_dir+"/baseline_corr/mW"
processed_csv_dir = './'+csv_dir+"-PROCESSED_baseline/processed_csv"

dir_create = [processed_dir,graph_dir,baseline_dir,baseline_dir_mw,processed_csv_dir]

for i in dir_create:
    if not os.path.exists(i):
        os.makedirs(i)

# if not os.path.exists(csv_dir):
#     os.makedirs(csv_dir)
# if not os.path.exists(processed_dir):
#     os.makedirs(processed_dir)
# if not os.path.exists(graph_dir):
#     os.makedirs(graph_dir)





#loop through each csv in unprocessed files folder
for (path, names, fnames) in os.walk(csv_dir):
    for name in fnames:
        print(name)
        fpath = os.path.join(path, name)
        
        #returns [cleaned_data,averaged_data] - each array has columns for wavelengfth and power; cleaned data column 0 is time
        processed_data = cleanupV2_2_unorderedWL.cleanup(name,fpath,processed_csv_dir)
        # processed_data = cleanupV2_1_module.cleanup(name,fpath,processed_dir)

        #create single dimensional arrays for plotting

        wl_plot = []
        power_plot = []

        ave_wl_plot = []
        ave_power_plot = []


        for data_point in processed_data[0][0:]:
        
            wl_plot.append(float(data_point[1]))
            power_plot.append(float(data_point[2]))

        for data_point in processed_data[1][0:]:
        
            ave_wl_plot.append(float(data_point[0]))
            ave_power_plot.append(float(data_point[1]))

        name = name[0:-4]       
        # plt.figure(figsize=(15,7))
        # plt.plot(wl_plot)
        # plt.title(name)
        # plt.grid(alpha=0.7)
        # plt.show()
        # # plt.clf()
        # plt.close()

        plt.figure(figsize=(15,7))
        plt.plot(ave_wl_plot,ave_power_plot)
        plt.title(name+"_average")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (dBm)")
        plt.grid(alpha=0.7)
        plt.savefig(graph_dir+"/"+name+"_average.png")
        # plt.show()
        plt.close()

        plt.figure(figsize=(15,7))
        plt.plot(wl_plot,power_plot)
        plt.title(name+"_linegraph")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (dBm)")
        plt.grid(alpha=0.7)
        plt.savefig(graph_dir+"/"+name+"_linegraph.png")
        # plt.show()
        plt.close()

        plt.figure(figsize=(15,7))
        plt.scatter(wl_plot,power_plot)
        plt.title(name+"_scatter")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (dBm)")
        plt.grid(alpha=0.7)
        plt.savefig(graph_dir+"/"+name+"_scatter.png")
        # plt.show()
        plt.close()

        np_power = np.array(ave_power_plot)
        
        #
        power_bsln = pybaselines.polynomial.imodpoly(ave_power_plot,poly_order=4)[0] #get baseline
        bl_corrected_power = np.subtract(np_power,power_bsln) #subtract baseline
        bl_corrected_power = bl_corrected_power-np.max(bl_corrected_power) #normalize
        plt.figure(figsize=(15,7))
        plt.plot(ave_wl_plot,bl_corrected_power)
        # plt.plot(ave_wl_plot,ave_power_plot)
        plt.title(name+"_baseline_corrected")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (dBm)")
        plt.grid(alpha=0.7)
        plt.savefig(baseline_dir+"/"+name+"_baseline_corrected.png")
        # plt.show()
        plt.close()

        
        bl_corrected_power_mw = logtomw(bl_corrected_power)
        ave_power_plot_mw = logtomw(ave_power_plot)
        plt.figure(figsize=(15,7))
        plt.plot(ave_wl_plot,bl_corrected_power_mw)
        # plt.plot(ave_wl_plot,ave_power_plot_mw)
        plt.title(name+"_baseline_corrected_mw")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (mW)")
        plt.grid(alpha=0.7)
        plt.savefig(baseline_dir+"/"+name+"_baseline_corrected_mW.png")
        # plt.show()
        plt.close()

input("Enter to Continue")
        

        