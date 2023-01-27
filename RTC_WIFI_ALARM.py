import network
from mywifi import networksetting
from machine import RTC
from time import sleep
import rp2
import sys
import utime as time
import usocket as socket
import ustruct as struct

ssid, password = networksetting()

# Winterzeit / Sommerzeit
GMT_OFFSET = 3600 * 1 # 3600 = 1 h (Winterzeit)
#GMT_OFFSET = 3600 * 2 # 3600 = 1 h (Sommerzeit)

# NTP-Host
NTP_HOST = 'pool.ntp.org'



# Funktion: get time from NTP Server
def getTimeNTP():
    NTP_DELTA = 2208988800
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    ntp_time = struct.unpack("!I", msg[40:44])[0]
    return time.gmtime(ntp_time - NTP_DELTA + GMT_OFFSET)

# Funktion: copy time to PI pico´s RTC
def setTimeRTC():
    tm = getTimeNTP()
    rtc.datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

def check_alarm(set_year,set_month,set_day,set_hour,set_minute):
    time = rtc.datetime()
    if set_year == int(time[0]) and set_month == int(time[1]) and set_day == int(time[2]) and set_hour == int(time[4]) and set_minute == int(time[5]):
        print("ALARM")
    else:
        print("Time not reached")
        print("time now " + str(time))
        print("time to alarm:  " + str(set_year) +" " + str(set_month) + " " + str(set_day) + " " + str(set_hour) + " " + str(set_minute))

  
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
    
max_wait = 10
print('Waiting for connection')
while max_wait > 10:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1    
    sleep(1)
status = None
if wlan.status() != 3:
    raise RuntimeError('Connections failed')
else:
    status = wlan.ifconfig()
    print('connection to', ssid,'succesfull established!', sep=' ')
    print('IP-adress: ' + status[0])
ipAddress = status[0]
    

rtc = RTC()  

# Zeit setzen
setTimeRTC()

# Aktuelles Datum ausgeben
print()
print(rtc.datetime())

while True:
    year=2023
    month=1
    day=20
    hour=20
    minute=18
    check_alarm(year,month,day,hour,minute)
    sleep(10)




