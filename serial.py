import serial, time
port="/dev/cu.usbmodem14201"
baudrate=9600

newserial = serial.Serial(port=port, baudrate=baudrate)
time.sleep(2)
arduino.write(b'9')
arduino.close()