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
int = i = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)


def repeat ():
    Cycle = 0
    while True:
        spi.writebytes([0x0B,0x0F,0x1C,0x8E,0xEB])
        #Write register 0B as 177MHz
        GPIO.output(22,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(22,GPIO.LOW)
        #IO Updtae Pulse
        time.sleep(10)
        spi.writebytes([0x0B,0x11,0x13,0x40,0x96])
        #Write register 0B as 200MHz
        GPIO.output(22,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(22,GPIO.LOW)
        #IO Updtae Pulse
        time.sleep(10)   
        Cycle = Cycle+1
        print(Cycle)
    
try:

                
        
        GPIO.output(17,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(17,GPIO.LOW)
        #Reset Pulse
        #time.sleep(0.001)
        
        GPIO.output(27,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(27,GPIO.LOW)
        #IO Sync Pulse
        
        spi.writebytes([0x03,0x03,0x05,0x21,0x20])
        #DAC calibration
        
        GPIO.output(22,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(22,GPIO.LOW)
        time.sleep(0.001)
        #IO Update Pulse
        
        spi.writebytes([0x03,0x00,0x05,0x21,0x20])
        #DAC calibration clear bit
        
        GPIO.output(22,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(22,GPIO.LOW)
        #IO Updtae Pulse
        
        spi.writebytes([0x00,0x00,0x01,0x00,0x0A])
        #Write register 00
        
        spi.writebytes([0x01,0x00,0x80,0x09,0x00])
        #Write register 01
        
        spi.writebytes([0x02,0x00,0x00,0x19,0x1C])
        #Write register 02
        
        spi.writebytes([0x0B,0x0F,0x1C,0x8E,0xEB])
        #Write register 0B
        
        GPIO.output(22,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(22,GPIO.LOW)
        #IO Updtae Pulse   
        
        for x in reg:
            spi.writebytes([reg[i]])
            print(reg[i])
            resp=spi.readbytes(4)
            print('Received 0x{0}'.format(binascii.hexlify(bytearray(resp))))
            print(resp[0:5])
            i=i+1   
        
        repeat()
            
 
        
finally:
    spi.close()
    

