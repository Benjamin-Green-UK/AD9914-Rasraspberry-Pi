#!../../bin/linux-aarch64/SPI_test

#- You may have to change SPI_test to something else
#- everywhere it appears in this file

< envPaths
epicsEnvSet( "STREAM_PROTOCOL_PATH", "$(TOP)/protocol" )

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/SPI_test.dbd"
SPI_test_registerRecordDeviceDriver pdbbase

## Load record instances
#dbLoadRecords("db/xxx.db","user=greenbt2")
GpioConstConfigure("RASPI B+")
drvAsynSPIConfigure( "SPI", "/dev/spidev0.0", 0, 10000000, 1 )

dbLoadRecords( "$(TOP)/db/SPI_test.db","head=greenbt2" )
cd "${TOP}/iocBoot/${IOC}"
iocInit

#var streamDebug 1
#asynSetTraceMask( "SPI", 0, 10 )
#asynSetTraceIOMask( "SPI", 0, 10 )

## Start any sequence programs
#seq sncxxx,"user=greenbt2"
