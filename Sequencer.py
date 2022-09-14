import time 
import epics
from epics import caget, caput, cainfo
from epics import PV
import binascii

first = ["3", "3", "0", "1", "2"]
second = ["3", "0", "0", "0", "0"]
third = ["5", "5", "1", "128", "0"]
fourth = ["33", "33", "0", "9", "25"]
fifth = ["32", "32", "10", "0", "28"]
#Byte values for the setup function. Read virtically 

c = ['11', '0', '0', '0', '0'] #Byte values to set register 11 to 0
d = 0
e = 0 #Will be used as counters later
temp = 0
pwr = 2**32 #Quicker to declare this here


def I_O_UPpdate():
	caput('greenbt2:GPIO22:OUT', 'ON')
	time.sleep(0.0001)
	caput('greenbt2:GPIO22:OUT', 'OFF')
	#IO Update Pulse

def start_up():
	global first, second, third, fourth, fifth
	caput('greenbt2:GPIO17:OUT', 'ON')
	time.sleep(0.0001)
	caput('greenbt2:GPIO17:OUT', 'OFF')
	time.sleep(0.001)
	#Reset Pulse
	
	caput('greenbt2:GPIO27:OUT', 'ON')
	time.sleep(0.0001)
	caput('greenbt2:GPIO27:OUT', 'OFF')
	time.sleep(0.0001)
	#IO Sync Pulse
	
	i = 0
	
	for x in first:
		caput('TEST:BYTE1', first[i])
		caput('TEST:BYTE2', second[i])
		caput('TEST:BYTE3', third[i])
		caput('TEST:BYTE4', fourth[i]) #Sets four of the byte values in EPICS
		caput('greenbt2:GPIO18:OUT', 'ON')
		caput('greenbt2:GPIO23:OUT', 'ON')
		caput('greenbt2:GPIO24:OUT', 'ON')
		caput('greenbt2:GPIO25:OUT', 'ON') #Turns on all the CS lines for four AD9914 boards
		caput('TEST:BYTE5', fifth[i]) #After the fifth byte is set in EPICS, it sends all five bytes
		time.sleep(0.001) #Makes sure no timing errors occur
		caput('greenbt2:GPIO18:OUT', 'OFF') 
		caput('greenbt2:GPIO23:OUT', 'OFF')
		caput('greenbt2:GPIO24:OUT', 'OFF')
		caput('greenbt2:GPIO25:OUT', 'OFF') #Turn off all CS lines
		I_O_UPpdate() #Moves the values from the serial buffer to the registers 
		i = i+1
start_up()

def onChanges(pvname=None, value=None, char_value=None, **kw):
	print('PV Changed!', pvname, char_value, time.ctime())
	Value_PV = float(char_value) #When the value of the frequency PV changes 
	print(Value_PV)
	FTW = int(round(2**32*(Value_PV/((2998.5*10**6))))) #Calculates the FTW to be sent via SPI
	print(FTW)
	FTW_bytes = FTW.to_bytes(4, 'big') #Converts to four bytes
	print(FTW_bytes)
	b= list(FTW_bytes)
	print(b)
	global c
	c[1] = str(b[0])
	c[2] = str(b[1])
	c[3] = str(b[2])
	c[4] = str(b[3]) #Moves the byte values to a global array 
	global d
	global e 
	d = e
	d = d+1 #Makes d != e to indicate the value has been changed
mypv = epics.PV('INPUT:FREQ') #Links the PV to the Input Frequency EPICS record
mypv.add_callback(onChanges) #Uses a callback to activate the onChanges function when the PV changes

def send():
	global d
	global e
	global temp 	
	if d == 100000:
		d = 1
		e = 0 #Stops the values increasing without bound 
	if d != e:
		#When d != e, need to send the new value 
		caput('TEST:BYTE1.VAL', c[0])
		caput('TEST:BYTE2.VAL', c[1])
		caput('TEST:BYTE3.VAL', c[2])
		caput('TEST:BYTE4.VAL', c[3])
		#Set the first four bytes
		if caget('CS1.VAL') == 1:
			caput('greenbt2:GPIO18:OUT', 'ON')
			#Puts CS line 1 on to write to DDS board 1 
		if caget('CS2.VAL') == 1:
			caput('greenbt2:GPIO23:OUT', 'ON')
			#Puts CS line 2 on to write to DDS board 2
		if caget('CS3.VAL') == 1:
			caput('greenbt2:GPIO24:OUT', 'ON')
			#Puts CS line 3 on to write to DDS board 3
		if caget('CS4.VAL') == 1:
			caput('greenbt2:GPIO25:OUT', 'ON')
			#Puts CS line 4 on to write to DDS board 4
		caput('TEST:BYTE5.VAL', c[4])
		#Sets the fifth byte which sends the SPI signal 
		caput('greenbt2:GPIO25:OUT', 'OFF')#25
		caput('greenbt2:GPIO24:OUT', 'OFF')#24
		caput('greenbt2:GPIO23:OUT', 'OFF')#23
		caput('greenbt2:GPIO18:OUT', 'OFF')#18
		#Must be turned off in this order due to timing 
		I_O_UPpdate()
		
		#Read back procedure 
		if caget('CS1.VAL') == 1: #18
			caput('greenbt2:GPIO18:OUT', 'ON') #Puts CS line 1 on 
			temp = caget('READ:SWITCH.VAL') #Gets the current value of the read switch
			temp = temp+1 #When temp changes, EPICS has a forward link to the record which activated the read function 
			time.sleep(0.001) #Timing here is critical, must give the CS line extra on time to account for timing variations in the read pulses
			caput('READ:SWITCH.VAL', temp) #Changes the read switch value to activate the read function in EPICS
			time.sleep(0.01) #Critical for timing variation
			caput('greenbt2:GPIO18:OUT', 'OFF') #Turn of CS line 1
				
		if caget('CS2.VAL') == 1: #23
			caput('greenbt2:GPIO23:OUT', 'ON')
			temp = caget('READ:SWITCH2.VAL') 
			temp = temp+1
			time.sleep(0.001)
			caput('READ:SWITCH2.VAL', temp)
			time.sleep(0.01)
			caput('greenbt2:GPIO23:OUT', 'OFF')		
		
		if caget('CS3.VAL') == 1:
			caput('greenbt2:GPIO24:OUT', 'ON')
			temp = caget('READ:SWITCH3.VAL') 
			temp = temp+1
			time.sleep(0.001)
			caput('READ:SWITCH3.VAL', temp)
			time.sleep(0.01)
			caput('greenbt2:GPIO24:OUT', 'OFF')
		
		if caget('CS4.VAL') == 1:
			caput('greenbt2:GPIO25:OUT', 'ON')
			temp = caget('READ:SWITCH4.VAL') 
			temp = temp+1
			time.sleep(0.001)
			caput('READ:SWITCH.VAL4', temp)
			time.sleep(0.01)
			caput('greenbt2:GPIO25:OUT', 'OFF')
		
		if temp > 50000:
			caput('READ:SWITCH.VAL', 0)
			caput('READ:SWITCH2.VAL', 0)
			caput('READ:SWITCH3.VAL', 0)
			caput('READ:SWITCH4.VAL', 0)
			#Stops values increasing without bound
		e = e+1
		#Makes e = d, read/write is now finished 
		
		
	
def main():
	while True:
		global pwr
		send()
		time.sleep(0.001)
		if caget('CS1.VAL') == 1:
			#Performs the calculation to change the FTW into a readable frequency, must be performed in this function 
			caput('CHANNEL1:FREQ', (caget('READ:BACK.VAL')/(pwr))*(2998.5*10**6))
			time.sleep(0.001)
		if caget('CS2.VAL') == 1:
			caput('CHANNEL2:FREQ', (caget('READ:BACK2.VAL')/(2**32))*(2998.5*10**6))
			time.sleep(0.001)
		if caget('CS3.VAL') == 1:
			caput('CHANNEL3:FREQ', (caget('READ:BACK3.VAL')/(2**32))*(2998.5*10**6))
			time.sleep(0.001)
		if caget('CS4.VAL') == 1:
			caput('CHANNEL4:FREQ', (caget('READ:BACK4.VAL')/(2**32))*(2998.5*10**6))
			time.sleep(0.001)
		send()

		
	

main()		
