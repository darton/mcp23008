#!/usr/bin/env python3

from pid import PidFile
import threading
import smbus
import ctypes
from gpiozero import Button
from signal import pause
from time import sleep
import subprocess as sp
from mcp23008 import *


def clear_interrupt():
    intcap = bus.read_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_INTCAP)

def init_mcp23008():
    bus.write_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_IODIR, MCP23008_IODIR_PIN_INPUT)
    bus.write_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_GPPU, MCP23008_GPPU_PIN_EN)
    bus.write_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_GPINTEN, 0xFF)
    bus.write_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_INTCON, 0x00)
    bus.write_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_IOCON, 0x3A)
    bus.write_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_DEFVAL, 0x00)
    #intf = bus.read_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_INTF)
    #intcap = bus.read_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_INTCAP)

def interrupt_handling():
    t = threading.Thread(target=do_something)
    t.daemon = True
    t.start()

def do_something():
    read_gpio()
    print_on_screen()

def read_gpio():
    global mcp_gpio
    mcp_gpio = bus.read_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_GPIO)

def print_on_screen():
    sp.call('clear',shell=True)
    pins = Flags()
    pins.asByte = mcp_gpio
    print("When button is pressed you'll see a message")
    print("")
    print("Input 1 = %i" % pins.bit0)
    print("Input 2 = %i" % pins.bit1)
    print("Input 3 = %i" % pins.bit2)
    print("Input 4 = %i" % pins.bit3)
    print("Input 5 = %i" % pins.bit4)
    print("Input 6 = %i" % pins.bit5)
    print("Input 7 = %i" % pins.bit6)
    print("Input 8 = %i" % pins.bit7)

def get_url():
    pins = Flags()
    pins.asByte = mcp_gpio
    input_id = 50
    if pins.bit0 == 1:
        response = urlopen('https://127.0.0.1/json.htm?type=command&param=udevice&idx=' + str(input_id) + '&svalue=1', context=ssl._create_unverified_context())
    else:
        response = urlopen('https://127.0.0.1/json.htm?type=command&param=udevice&idx=' + str(input_id) + '&svalue=0', context=ssl._create_unverified_context())


c_uint8 = ctypes.c_uint8

class Flags_bits( ctypes.LittleEndianStructure ):
    _fields_ = [
                 ("bit0", c_uint8, 1 ),  # asByte & 1
                 ("bit1", c_uint8, 1 ),  # asByte & 2
                 ("bit2", c_uint8, 1 ),  # asByte & 4
                 ("bit3", c_uint8, 1 ),  # asByte & 8
                 ("bit4", c_uint8, 1 ),  # asByte & 16
                 ("bit5", c_uint8, 1 ),  # asByte & 32
                 ("bit6", c_uint8, 1 ),  # asByte & 64
                 ("bit7", c_uint8, 1 ),  # asByte & 128
               ]

class Flags( ctypes.Union ):
    _anonymous_ = ("bit",)
    _fields_ = [
                 ("bit",    Flags_bits ),
                 ("asByte", c_uint8    )
                ]

# --- Main program ---
with PidFile(piddir='/tmp/'):

# Get I2C bus
    bus = smbus.SMBus(1)

    init_mcp23008()
    clear_interrupt()

    mcp_gpio = 0xFF
    interrupt = Button(27, pull_up=False, hold_time=0.001)

    print_on_screen()

    interrupt.when_pressed = interrupt_handling
    interrupt.when_held = clear_interrupt

    pause()
