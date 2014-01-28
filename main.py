import serial
import os
import struct
import time
init = "\xff\xff\xef"
stop = "\xf0"
dtc = "\xd1\xf0"
shutup = "\x30\xf0" 

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
#I don't even use this...
def Reed():
    while 1:
        if ser.inWaiting():
            print ser.read(1).encode('hex')
        else:
            waittime = raw_input("Press Enter to Continue")
ser.close()
ser.open()
ser.write(init)
resp =  ser.read(1).encode('hex')
if resp == "10":
    print "INITIALIZATION COMPLETE"
elif resp == "00":
    print "ALREADY INITIALIZED"
else:
    ser.write(shutup)
    while 1:
        if ser.inWaiting():
            if ser.read(1).encode('hex') == "cf":
                break
        else:
            time.sleep(0.1)
            if not ser.inWaiting():
                break
    ser.write(init)
    resp =  ser.read(1).encode('hex')
    if resp == "10":
        print "INITIALIZATION COMPLETE"
    elif resp == "00":
        print "ALREADY INITIALIZED"
    else:
        print "WHAT THE HELL THIS SHIT IS BROKE"
        quit()
print "READIN THEM ERROR CODES"
ser.write(dtc)
while 1:
    if ser.read(1).encode('hex') == "ff":
        ser.write(shutup)
        break
response = []
while 1:
    if ser.inWaiting():
        response.append(ser.read(1).encode('hex'))
    else:
        time.sleep(0.1)
        if not ser.inWaiting():
            break
m = int(response[0], 16) - 1
starterror = ""
if m == 1:
    if response[m] == "55":
        print "NO ERRORS, CONGRATS"
    else:
        print "You recieved ",m," error codes! They are:"
        while m > 0:
            print response[m]
            starterror += str(response[m])
            m = m - 1
        print " THOSE ARE YOUR ERROR CODES"

#ser.write("\xd0\xf0")
#while 1:
#    if ser.read(1).encode('hex') == "ff":
#	ser.write(shutup)
#	break
#response = []
#while 1:
#    if ser.inWaiting():
#	response.append(ser.read(1).encode('hex'))
#    else:
#	time.sleep(0.1)
#	if not ser.inWaiting():
#	    break
#print "ECU info"
#print response



##LETS SEE IF WE CAN READ TACH!

#ser.write("\x5a\x01\x5a\x08\xf0")
##while 1:
##    if ser.read(1).encode('hex') == "ff":
##	ser.write(shutup)
##	break
#time.sleep(0.5)
#ser.write(shutup)
#response = []
#while 1:
#    if ser.inWaiting():
#	response.append(ser.read(1).encode('hex'))
#    else:
#	time.sleep(0.1)
#	if not ser.inWaiting():
#	    break
#print "x00 then x01"
#print response

print "LETS TRY LIVE READING"
#ser.write("\x5a\x15\xf0")
#while 1:
#    if ser.read(1).encode('hex') == "ff":
#	break
#while 1:
#    mainrep = ser.read(3).encode('hex')
#    injtim = int(mainrep, 16) / 100
#    os.system('clear')
#    print "Current injector timing is ", injtim, " mS"
#ser.write("\x5a\x01\x5a\x08\x5a\x05\xf0")

ser.write("\x5a\x01\x5a\x08\x5a\x00\x5a\x05\x5a\x04\x5a\x14\x5a\x15\x5a\x0b\xf0")
##NOTES
#x01 = Tach MSB
#x02 = Tach LSB
#x04 = MAF MSB
#x05 = MAF LSB
#x08 = Coolant Temp
#x0b = Vehicle Speed
#x14 = Injector Pulse Time MSB
#x15 = Injector Pulse Time LSB
#Need to precede each streaming item with \x5a
#ser.write("\x5a\x01\x5a\x08\x5a\x15\xf0")
while 1:
    if ser.read(1).encode('hex') == "ff":
        break
while 1:
    mainrep = []
    prerep = ser.read(200)
    for item in prerep:
        mainrep.append(item.encode('hex'))
    while 1:
        if mainrep[0] == "08":
            break
       else:
           del mainrep[0]
    revlsb = int(mainrep[3], 16) * 12.5 * 256
    rev = int(mainrep[1], 16) * 12.5 + revlsb
    celtemp = int(mainrep[2], 16) - 50
    injlsb = int(mainrep[6], 16) * .01 * 255
    injtim = int(mainrep[7], 16) * .01 + injlsb
    maflsb = int(mainrep[5], 16) * 5 *256
    mafvolt = int(mainrep[4], 16) * 5 + maflsb
    speedo = int(mainrep[8], 16) * 2 * 0.621371
    ftemp = celtemp * 9/5 + 32
    os.system('clear')
    #print mainrep[0]
    #print mainrep
    #print "Rev LSB is currently: ", revlsb
    print "Tach: ", rev, "RPM"
    print "Temp: ", ftemp, " F"
    print "Inj Timing: ", injtim, " mS"
    print "MAF Voltage: ", mafvolt, "mV"
    print "Speed: ", speedo," mph"
    print "Start Errors: ", starterrors
    #Need to figure out how to update the errors every so often for when i get NEW check engine lights





# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
