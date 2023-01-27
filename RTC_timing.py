from machine import RTC

rtc=RTC()

rtc.datetime((2023,01,20,4,18,14,0,0))

print(rtc.datetime())
