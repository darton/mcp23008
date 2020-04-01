# mcp23008
Use CP23008 as Raspberry Pi inputs expander based on GPIOZERO library.

Optionally, to improve permformance, increase the I2C baudrate from the default of 100KHz to 400KHz by altering /boot/config.txt to include:
```
dtparam=i2c_arm=on,i2c_baudrate=400000
```
