import os
# import cleanupV2_1_module
import cleanupV2_2_unorderedWL
import matplotlib.pyplot as plt
import numpy as np
import pybaselines


#create directories
csv_dir = "./unprocessed-6-19-24"
processed_dir = './processed-6-19-24'
# csv_dir = "./unprocessed"
# processed_dir = './processed'
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)




#loop through each csv in unprocessed files folder
for (path, names, fnames) in os.walk(csv_dir):
    for name in fnames:
        print(name)
        fpath = os.path.join(path, name)
        
        #returns [cleaned_data,averaged_data] - each array has columns for wavelength and power; cleaned data column 0 is time
        processed_data = cleanupV2_2_unorderedWL.cleanup(name,fpath,processed_dir)
        # processed_data = cleanupV2_1_module.cleanup(name,fpath,processed_dir)

        #create single dimensional arrays for plotting

        wl_plot = []
        power_plot = []

        ave_wl_plot = []
        ave_power_plot = []


        for data_point in processed_data[0][1:]:
        
            wl_plot.append(float(data_point[1]))
            power_plot.append(float(data_point[2]))

        for data_point in processed_data[1][1:]:
        
            ave_wl_plot.append(float(data_point[0]))
            ave_power_plot.append(float(data_point[1]))

        name = name[0:-4]       
        plt.figure(figsize=(15,7))
        plt.plot(wl_plot)
        plt.title(name)
        plt.grid(alpha=0.7)
        # plt.show()
        # plt.clf()
        plt.close()

        plt.figure(figsize=(15,7))
        plt.plot(ave_wl_plot,ave_power_plot)
        plt.title(name+"_average")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (dBm)")
        plt.grid(alpha=0.7)
        plt.savefig(processed_dir+"/"+name+"_average.png")
        # plt.show()
        plt.close()

        plt.figure(figsize=(15,7))
        plt.plot(wl_plot,power_plot)
        plt.title(name+"_linegraph")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (dBm)")
        plt.grid(alpha=0.7)
        plt.savefig(processed_dir+"/"+name+"_linegraph.png")
        # plt.show()
        plt.close()

        plt.figure(figsize=(15,7))
        plt.scatter(wl_plot,power_plot)
        plt.title(name+"_scatter")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (dBm)")
        plt.grid(alpha=0.7)
        plt.savefig(processed_dir+"/"+name+"_scatter.png")
        # plt.show()
        plt.close()

        np_power = np.array(power_plot)
        power_bsln_corr = pybaselines.Baseline.asls(np_power)
        plt.figure(figsize=(15,7))
        plt.plot(wl_plot,power_bsln_corr)
        plt.title(name+"_baseline_corrected")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Output Power (dBm)")
        plt.grid(alpha=0.7)
        # plt.savefig(processed_dir+"/"+name+"_baseline_corrected.png")
        plt.show()
        plt.close()

        

input("Enter to Continue")
        

        