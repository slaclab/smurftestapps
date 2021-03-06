##############################################################################
## This file is part of 'smurftestapps'.
## It is subject to the license terms in the LICENSE.txt file found in the 
## top-level directory of this distribution and at: 
##    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
## No part of 'smurftestapps', including this file, 
## may be copied, modified, propagated, or distributed except according to 
## the terms contained in the LICENSE.txt file.
##############################################################################

#make_config_file.py

#Edit this python script to generate smurf2mce.cfg config files
#copy file tot .../mcetransmit/smurf2mce.cfg
#most changese take effect while running
#ip or port changes require a smurf restart
import sys

docstring = """Program to genreate config files for the smurf mcetransmit program.  
Use:    python3 make_config_file <dev / prod> frame_rate  filter_lowpass_frequency filter_order receiver_ip_address output file nam3e
example:
python3 make_config_file.py  dev
writes a file called development.cfg which will create data files names /tmp/data.txt   Overwriting for each new file.  This is useful if you want to take, then analyze data.
defaults to 4000Hz frame rate, 63Hz low pass, 4th order 

python3 make_config_file.py prod 6000 60 4 192.168.3.34 /usr/local/controls/Applications/smurf/smurf2mce/current/mcetransmit/smurf2mce.cfg

Writes a file called production.cfg which will create data files in /data/smurf_stream/data_XXXXX.dat  where XXXX is the unix time stamp when th file was created
This assmes a 6KHz frame rate, 60Hz low pass, 3rd order butterworth filter
Ip 192.168.3.34 is the targed MCE computer
File will be written dirctly to the production location
"""


if len(sys.argv) < 2:
    mode = 0 # general purpose
else:
    if (sys.argv[1].find('?') != -1):
        print(docstring)
        exit()
    if (sys.argv[1].find('prod') != -1):
        mode = 1  # production
    else: 
        mode = 0  # development

# output data filtering. Butterworth filter used
filter_order = 4;  # this is for a 4th order filter
smurf_frame_rate = 4000;  # set by timing sysetms
filter_frequency = 63;  # chosen filter low pass frequency.
receiver_ip = "tcp://192.168.3.134:5333"

if len(sys.argv) > 2:
    smurf_frame_rate = float(sys.argv[2])
if len(sys.argv) > 3:
    filter_frequency = float(sys.argv[3])
if len(sys.argv) > 4:
    filter_order = int(sys.argv[4])
if len(sys.argv) > 5:
    receiver_ip = sys.argv[5]

if mode == 0:
    cfg_file_name = 'development.cfg'
if mode == 1:
    cfg_file_name = 'production.cfg'
if len(sys.argv) > 6:
    cfg_file_name = sys.argv[6]
    
      
    



#can change name to generate other files, then copy to smurf2mce.cfg



#Receiver IP is the IP address where MCE data will be sent.  N
#Note that the address is a string (!!!!), not numbers


#port number is the port to use to communicate with MCE. It has to be the same
#as the port in ../mcereceiver/src/smurfrec.cfg
#It is a string, not a number
# if a non numerical value is entered, then TCP is disabled
port_number = "5333"

#SMuRF data at the output (averaged, driven by syncbox) rate will be
#sent to a file 
#if file_name_extend is set to 1, then unix time will be appended to the filen name
#data frams indicates how many output frames should go to a single file. 1000000
#is about as large as practical. (~hour of data).


if (mode == 1):
    file_name_extend = 1
    data_file_name = "/data/smurf_stream/data" # .dat will be appended
if (mode == 0):
    file_name_extend = 0 
    data_file_name = "/tmp/data"

data_frames = 2000000;  # up to 1000000 works. 



#If num_averages = 0,  SMuRF output frames to MCE are triggered by the sync box
# A new frame is generated for each syncword increment
# num_averages > 0,  then an output frame is generated for every num_averages 
#number of smurf frames

num_averages = 0;

#no user changes below here
################################################################################

print('writing file: ', cfg_file_name)
print('assumed smurf frame rate = ', smurf_frame_rate, "Hz")
print('filter frequency = ', filter_frequency, "Hz", filter_order, "order butterworth")


from scipy import signal
print(filter_order)
print(filter_frequency)
print(smurf_frame_rate)
b,a = signal.butter(filter_order, 2*filter_frequency / smurf_frame_rate)

with open(cfg_file_name, "w") as f:
    f.write("num_averages " + str(num_averages) + '\n');
    f.write("receiver_ip " + receiver_ip + '\n');
    f.write("port_number " + port_number + '\n')
    f.write("data_file_name " + data_file_name + '\n');
    f.write("file_name_extend " + str(file_name_extend) + '\n')
    f.write("data_frames " + str(data_frames) + '\n')
    f.write("filter_order " + str(filter_order) +"\n");
    for n in range(0,filter_order+1):
        f.write("filter_a"+str(n)+" "+str(a[n]) + "\n")
    for n in range(0,filter_order+1):
        f.write("filter_b"+str(n)+" "+str(b[n]) + "\n")


	
