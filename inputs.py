#!/usr/bin/env python3
import smbus
from gpiozero import Button
from signal import pause
import ctypes
from mcp23008 import *

# Get I2C bus
bus = smbus.SMBus(1)

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
    global mcp23008_gpio
    pins = Flags()
    pins.asByte = bus.read_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_GPIO)
    print("Input_1: %i" % pins.bit0)
    print("Input_2: %i" % pins.bit1)
    print("Input_3: %i" % pins.bit2)
    print("Input_4: %i" % pins.bit3)
    print("Input_5: %i" % pins.bit4)
    print("Input_6: %i" % pins.bit5)
    print("Input_7: %i" % pins.bit6)
    print("Input_8: %i" % pins.bit7)


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

lock = threading.Lock()

init_mcp23008()
clear_interrupt()

interrupt = Button(27, pull_up=False, hold_time=0.001)

interrupt.when_pressed = interrupt_handling
interrupt.when_held = clear_interrupt


print("When button is pressed you'll see a message")

pause()
