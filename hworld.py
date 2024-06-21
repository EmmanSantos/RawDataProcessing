import serial
import serial.tools.list_ports
from time import sleep

print("hello world")
ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Port: {port.device}")
    print(f"Description: {port.description}")
    print(f"Hardware ID: {port.hwid}\n")

print("Laser port is usually labeled as FTDI")
comport = "COM"+input("Enter laser COM port number: ")
print(comport)
laser_port = serial.Serial(comport)
laser_port.baudrate = 9600
laser_port.stopbits= 1
laser_port.parity = 'N'
laser_port.bytesize = 8
print(laser_port)

#laser_port.write(bytearray([0x00,0x01,0x01,0x00,0x14,0x16]))


ch_start = int(input("Channel Start: "))
ch_end = int(input("Channel End: "))
increment = -1 if ch_start>ch_end else 1
for i in range(ch_start,ch_end+increment,increment):
   
    ch_num = i
    datah = ch_num//256
    datal = ch_num%256
    send_array = bytearray([0x00,0x01,0x01,datah,datal,datah+datal+2])
    print("Channel Number: ",ch_num)
    print(send_array)
    laser_port.write(send_array)
    sleep(5)

input("Enter to continue")



# single bit stream from channel number
# ch_num = 18
# datah = ch_num//256
# datal = ch_num%256
# send_array = bytearray([0x00,0x01,0x01,datah,datal,datah+datal+2])
# print("Channel Number: ",ch_num)
# print(send_array)
# laser_port.write(send_array)