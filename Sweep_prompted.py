import serial
import serial.tools.list_ports
from time import sleep

sweep_timegap = 0
ch_start = 0
ch_end = 0
first_run_ind = 1
ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Port: {port.device}")
    print(f"Description: {port.description}")
    print(f"Hardware ID: {port.hwid}\n")

print("Laser port is usually labeled as SER=FTDI on the Hardware ID line")
comport = "COM"+input("Enter laser COM port number: ")
print(comport)
laser_port = serial.Serial(comport)
laser_port.baudrate = 9600
laser_port.stopbits= 1
laser_port.parity = 'N'
laser_port.bytesize = 8
print(laser_port)





def sweep():
    def param_set():
        print("\n \nSET SWEEP PARAMETERS")
        inp_loop = True
        while inp_loop:
            print("Refer to the spreadsheet in the C-Band Laser Gdrive folder for the equivalent wavelength \nChannel Start must be higher than channel end")
            arg_ch_start = int(input("Channel Start (1-100): "))
            arg_ch_end = int(input("Channel End (1-100): "))
            arg_sweep_timegap = int(input("Seconds per wavelength(Recommended is min. of 5s): "))
            if arg_ch_start>arg_ch_end and (arg_ch_end<=100) and arg_ch_start<=100 :
                break
            print("\nINVALID VALUE/S \n")   

        return [arg_ch_start,arg_ch_end,arg_sweep_timegap] 

    global first_run_ind
    global sweep_timegap
    global ch_start
    global ch_end

    
    if(first_run_ind == 1):
        [ch_start,ch_end,sweep_timegap] = param_set()
    else:
        print("\nLAST RUN PARMETERS")
        print("Channel Start: ",str(ch_start))
        print("Channel End: ",str(ch_end))
        print("Time bet. wavelengths: ",str(sweep_timegap))
        if(input("Would you like to enter new parameters?(y/n)").lower() == 'y'):
            [ch_start,ch_end,sweep_timegap] = param_set()
        
    increment = -1 if ch_start>ch_end else 1
    input("Press Enter to start sweep")  
    for i in range(ch_start,ch_end+increment,increment):
        ch_num = i
        datah = ch_num//256
        datal = ch_num%256
        send_array = bytearray([0x00,0x01,0x01,datah,datal,datah+datal+2])
        print("Channel Number: ",ch_num)
        print(send_array)
        laser_port.write(send_array)
        sleep(sweep_timegap)

    first_run_ind = 0
    print("\n \nSWEEP FINISHED")


cont_flag = 'y'
while(cont_flag.lower() == 'y' ):
    sweep()
    cont_flag = input("Start another run?(y/n)")
