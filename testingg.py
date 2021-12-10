#!/bin/python3
import logi_led as logi_led
import time, sys, signal

from colour import Color
import ctypes

#Define Colors
red = Color("red")
green = Color("green")
grad = list(green.range_to(red,101))

#Catch CTRL+C / SIGINT
def signal_handler(sig,frame):
    print("EXIT")
    logi_led.logi_led_shutdown()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#Scale from 0.0/1.0 to 0/100
def led_color(r,g,b):
    logi_led.logi_led_set_lighting(int(r*100),int(g*100),int(b*100))

def start_up_led():
    led_color(1,0,0)
    time.sleep(.25)
    led_color(0,1,0)
    time.sleep(.25)
    led_color(0.3,0.3,0.3)
    time.sleep(.25)
    #led_color(.5,.5,.5)
    print("Init done")

logi_led.logi_led_init()
print(logi_led.led_dll)
time.sleep(1)
start_up_led()
print("Running CPU Monitor LED")


d = {"Q" : 0x10,
"W" : 0x11,
"E" : 0x12,
"R" : 0x13,
"T" : 0x14,
"Y" : 0x15,
"U" : 0x16,
"I" : 0x17,
"O" : 0x18,
"P" : 0x19,
"A" : 0x1e,
"S" : 0x1f,
"D" : 0x20,
"F" : 0x21,
"G" : 0x22,
"H" : 0x23,
"J" : 0x24,
"K" : 0x25,
"L" : 0x26,
"Z" : 0x2c,
"X" : 0x2d,
"C" : 0x2e,
"V" : 0x2f,
"B" : 0x30,
"N" : 0x31,
"M" : 0x32,}
try:
    while True:
            #update color to current CPU percenage

            inn = sys.stdin.read(1)
            sys.stdin.flush()
            inn=inn.upper()

            #key=chr(a).upper()


            
            #led_color(col.red,col.green,col.blue)
            print(logi_led.logi_led_set_lighting_for_key_with_key_name(d[str(inn)],int(0),int(200),int(210)))

            
            #print(logi_led.logi_led_pulse_single_key(int(logi_led.A),int(0),int(0),int(0),int(1000),True,int(100),int(200),int(210)))
            
except Exception as e:
    print(f"ERROR: {e}")
    logi_led.logi_led_shutdown()