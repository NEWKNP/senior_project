from time import sleep
import time
import os.path
import os
from datetime import date
from picamera import PiCamera
import RPi.GPIO as GPIO

day = 0 
hr = 0
start_date = 0
current_time = 0
previous_time = time.time()
interval = 3600

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)

camera = PiCamera()
camera.resolution = (2592, 1944)

#def start()

    


def update_day(new_day):
    with open('config.txt', 'r') as file:
        data = file.readlines()
    data[0] = ('%s\n' % new_day)
    with open('config.txt', 'w') as file:
        file.writelines(data)
        
def update_hr(new_hr):
    with open('config.txt', 'r') as file:
        data = file.readlines()
    data[1] = ('%s\n' % new_hr)
    with open('config.txt', 'w') as file:
        file.writelines(data)
        
def update_previous(new_previous):
    with open('config.txt', 'r') as file:
        data = file.readlines()
    data[3] = ('%s\n' % new_previous)
    with open('config.txt', 'w') as file:
        file.writelines(data)
        
def capture():
    sr = "%s/%s" % (start_date, day)
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/Microgreen/%s.jpg' % sr)
    camera.stop_preview()
  
def pre_cap():
    c_off()
    w_on()
    capture()
    if(day < 3):
        w_off()
    else:
        c_on()
    
def day_on():
    w_on()
    c_on()
  
def day_off():
    w_off()
    c_off()

def w_on():
    GPIO.output(17, 0)
    
def w_off():
    GPIO.output(17, 1)
    
def c_on():
    GPIO.output(27, 0)
    
def c_off():
    GPIO.output(27, 1)
    
def check():
    if ( day >= 3 and hr < 16 ):
        day_on()
    elif (day >= 3 and hr >= 16):
        day_off()
    else:
        day_off()
    
if os.path.isfile('config.txt'):
    file = open('config.txt')
    all_lines = file.readlines()
    day = int(all_lines[0])
    hr = int(all_lines[1])
    start_date = all_lines[2]
    previous_time = float(all_lines[3])
    check()
else :
    f = open('config.txt', "w+")
    f.write(str(day))
    f.write("\n")
    f.write(str(hr))
    f.write("\n")
    start_date = date.today()
    f.write(str(start_date))
    f.write("\n")
    f.write(str(previous_time))
    f.close()
    path = ("Microgreen/%s" % start_date) 
    try:
        os.mkdir(path)
    except OSError:
        print("fail")
    pre_cap()
try:
    while(True):
        current = time.time()
        if (current - previous_time >= 60):
            hr += 1
            check()
            if(hr > 23):
                hr = 0
                day += 1
                update_day(day)
                pre_cap()
            previous_time = current
            update_previous(previous_time)
            update_hr(hr)
            
except KeyboardInterrupt:
    print("done")
    
            
            
            
        


        
   
#main()