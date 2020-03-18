#!/usr/bin/env python3
import smbus
from gpiozero import Button
from signal import pause
from time import sleep

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
MCP23008_DEFAULT_ADDRESS                        = 0x20

# MCP23008 Register Map
MCP23008_REG_IODIR                                      = 0x00 # I/O DIRECTION Register
MCP23008_REG_IPOL                                       = 0x01 # INPUT POLARITY PORT Register
MCP23008_REG_GPINTEN                                    = 0x02 # INTERRUPT-ON-CHANGE PINS
MCP23008_REG_DEFVAL                                     = 0x03 # DEFAULT VALUE Register
MCP23008_REG_INTCON                                     = 0x04 # INTERRUPT-ON-CHANGE CONTROL Register
MCP23008_REG_IOCON                                      = 0x05 # I/O EXPANDER CONFIGURATION Register
MCP23008_REG_GPPU                                       = 0x06 # GPIO PULL-UP RESISTOR Register
MCP23008_REG_INTF                                       = 0x07 # INTERRUPT FLAG Register
MCP23008_REG_INTCAP                                     = 0x08 # INTERRUPT CAPTURED VALUE FOR PORT Register
MCP23008_REG_GPIO                                       = 0x09 # GENERAL PURPOSE I/O PORT Register
MCP23008_REG_OLAT                                       = 0x0A # OUTPUT LATCH Register 0

# MCP23008 I/O Direction Register Configuration
MCP23008_IODIR_PIN_7_INPUT                      = 0x80 # Pin-7 is configured as an input
MCP23008_IODIR_PIN_6_INPUT                      = 0x40 # Pin-6 is configured as an input
MCP23008_IODIR_PIN_5_INPUT                      = 0x20 # Pin-5 is configured as an input
MCP23008_IODIR_PIN_4_INPUT                      = 0x10 # Pin-4 is configured as an input
MCP23008_IODIR_PIN_3_INPUT                      = 0x08 # Pin-3 is configured as an input
MCP23008_IODIR_PIN_2_INPUT                      = 0x04 # Pin-2 is configured as an input
MCP23008_IODIR_PIN_1_INPUT                      = 0x02 # Pin-1 is configured as an input
MCP23008_IODIR_PIN_0_INPUT                      = 0x01 # Pin-0 is configured as an input
MCP23008_IODIR_PIN_INPUT                        = 0xFF # All Pins are configured as an input
MCP23008_IODIR_PIN_OUTPUT                       = 0x00 # All Pins are configured as an output

# MCP23008 Pull-Up Resistor Register Configuration
MCP23008_GPPU_PIN_7_EN                          = 0x80 # Pull-up enabled on Pin-7
MCP23008_GPPU_PIN_6_EN                          = 0x40 # Pull-up enabled on Pin-6
MCP23008_GPPU_PIN_5_EN                          = 0x20 # Pull-up enabled on Pin-5
MCP23008_GPPU_PIN_4_EN                          = 0x10 # Pull-up enabled on Pin-4
MCP23008_GPPU_PIN_3_EN                          = 0x08 # Pull-up enabled on Pin-3
MCP23008_GPPU_PIN_2_EN                          = 0x04 # Pull-up enabled on Pin-2
MCP23008_GPPU_PIN_1_EN                          = 0x02 # Pull-up enabled on Pin-1
MCP23008_GPPU_PIN_0_EN                          = 0x01 # Pull-up enabled on Pin-0
MCP23008_GPPU_PIN_EN                            = 0xFF # Pull-up enabled on All Pins
MCP23008_GPPU_PIN_DS                            = 0x00 # Pull-up disabled on All Pins

# MCP23008 General Purpose I/O Port Register
MCP23008_GPIO_PIN_7_HIGH                        = 0x80 # Logic-high on Pin-7
MCP23008_GPIO_PIN_6_HIGH                        = 0x40 # Logic-high on Pin-6
MCP23008_GPIO_PIN_5_HIGH                        = 0x20 # Logic-high on Pin-5
MCP23008_GPIO_PIN_4_HIGH                        = 0x10 # Logic-high on Pin-4
MCP23008_GPIO_PIN_3_HIGH                        = 0x08 # Logic-high on Pin-3
MCP23008_GPIO_PIN_2_HIGH                        = 0x04 # Logic-high on Pin-2
MCP23008_GPIO_PIN_1_HIGH                        = 0x02 # Logic-high on Pin-1
MCP23008_GPIO_PIN_0_HIGH                        = 0x01 # Logic-high on Pin-0
MCP23008_GPIO_PIN_HIGH                          = 0xFF # Logic-high on All Pins
MCP23008_GPIO_PIN_LOW                           = 0x00 # Logic-low on All Pins

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
    global int_flag
    if (int_flag == 0):
        int_flag = 1
        mcp23008_gpio = bus.read_byte_data(MCP23008_DEFAULT_ADDRESS, MCP23008_REG_GPIO)
        print(mcp23008_gpio)
        int_flag = 0

init_mcp23008()
clear_interrupt()

int_flag=0
interrupt = Button(27, pull_up=False, hold_time=0.01)

interrupt.when_pressed = interrupt_handling
interrupt.when_held = clear_interrupt

print("When button is pressed you'll see a message")

pause()
