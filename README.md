# AD9914-Rasraspberry-Pi
Library to control the AD9914 evaluation board in single tone mode with a Raspberry Pi using SPI. Contains both a Python approach and an EPICS approach. EPICS approach controls four AD9914 boards 

This repository contains work I completed as part of a summer internship project during 2022 and will not be updated. 
The spi_user_input code is the Python approach for controlling one AD9914 board via SPI using the spidev library. 
The robustness test was code developed to test the reliability of the SPI communication link and simply changes the frequency of the AD9914 board from a test tone of 177 MHz to 200Mhz and back indefinitely.

The EPICS approach uses the PyEPICS Python library found here https://github.com/pyepics/pyepics, the devGPIO device support version R1-0-6 found here https://github.com/ffeldbauer/epics-devgpio/tree/R1-0-6
and the drvAsynSPI device support found here https://github.com/kek-acc/drvAsynSPI. 

The EPICS approach uses the SPI_final IOC with the Python sequencer running in parrallel on the same board. 
The PCB Gerber WILL NOT WORK with the IOC and sequencer here. 
Edits suggested in the documentation will provide a solution to get the IOC and PCB to work together.

