import spidev
import time
import binascii
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz= 10000000
spi.threewire = False
spi.mode = 0

reg = bytearray(b'\x80\x81\x82\x83\x8B\x8C')
#Byte array with each address for the start up procedure

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
#Sets up the GPIO pins to output

def I_O_Update():
        GPIO.output(22,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(22,GPIO.LOW)
        time.sleep(0.001)
        #IO Update Pulse
    
def start_up() :
        GPIO.output(17,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(17,GPIO.LOW)
        #Reset Pulse
                
        GPIO.output(27,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(27,GPIO.LOW)
        #IO Sync Pulse
        
        spi.writebytes([0x03,0x03,0x05,0x21,0x20])
        #DAC calibration
        
        I_O_Update()
        #I/O Update Pulse      
        
        spi.writebytes([0x03,0x00,0x05,0x21,0x20])
        #DAC calibration clear bit
        
        I_O_Update()
        #IO Updtae Pulse
        
        spi.writebytes([0x00,0x00,0x01,0x00,0x0A])
        #Write register 00
        
        spi.writebytes([0x01,0x00,0x80,0x09,0x00])
        #Write register 01
        
        spi.writebytes([0x02,0x00,0x00,0x19,0x1C])
        #Write register 02
        
        spi.writebytes([0x0B,0x00,0x00,0x00,0x00])
        #Write register 0B
        
        I_O_Update()
        #IO Updtae Pulse 

def read_back() :
    int = i = 0
    for x in reg:
        spi.writebytes([reg[i]])
        print(reg[i])
        resp=spi.readbytes(4)
        print('Received 0x{0}'.format(binascii.hexlify(bytearray(resp))))
        print(resp[0:5])
        i=i+1
        #Reads back the data in the setup registers and register 11
    
def input_frequency() :
    while True:
        frequency = float(input("Please enter a frequency in MHz "))
        frequency = frequency * 1000000
        FTW = int(round(2**32*(frequency/((2998.5*10**6)))))
        #Calculate the frequency tuning word
        FTW_hex = hex(FTW)
        print(frequency,FTW,FTW_hex)
        print(type(FTW_hex))
        #Shows in a readable format
        FTW_bytes = FTW.to_bytes(4, 'big')
        print(FTW_bytes)
        #Convert to four bytes
        b = list(FTW_bytes)
        print(b)
        c = bytes(b)
        print(c)
        #Now in a sendible format
        k = int(0)
        spi.writebytes([0x0B])
    
        for x in FTW_bytes:
            spi.writebytes([c[k]])
            k=k+1
            #Send new bytes
        I_O_Update()
        read_back()
        
try:
    start_up()
    GPIO.output(27,GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(27,GPIO.LOW)
    read_back()
    input_frequency()
    
finally:
    spi.close()
    
