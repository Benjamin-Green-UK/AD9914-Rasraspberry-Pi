TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = SPI_test
# SPI_test.dbd will be created and installed
DBD += SPI_test.dbd

# SPI_test.dbd will be made up from these files:
SPI_test_DBD += base.dbd

# Include dbd files from all support applications:
#SPI_test_DBD += xxx.dbd
SPI_test_DBD += asyn.dbd
SPI_test_DBD += stream.dbd
SPI_test_DBD += devgpio.dbd
SPI_test_DBD += drvAsynSPI.dbd

# Add all the support libraries needed by this IOC
#SPI_test_LIBS += xxx
SPI_test_LIBS += asyn
SPI_test_LIBS += stream
SPI_test_LIBS += devgpio
SPI_test_LIBS += drvAsynSPI

# SPI_test_registerRecordDeviceDriver.cpp derives from SPI_test.dbd
SPI_test_SRCS += SPI_test_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
SPI_test_SRCS_DEFAULT += SPI_testMain.cpp
SPI_test_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#SPI_test_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
SPI_test_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

