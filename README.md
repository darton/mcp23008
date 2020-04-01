# mcp23008
Use MCP23008 as Raspberry Pi inputs expander based on GPIOZERO library.

Optionally, to improve permformance, increase the I2C baudrate from the default of 100KHz to 400KHz by altering /boot/config.txt to include:
```
dtparam=i2c_arm=on,i2c_baudrate=400000
```
Next check that the device is communicating properly.

```
$ i2cdetect -y 1
       0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
  00:          -- -- -- -- -- -- -- -- -- -- -- -- --
  10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  20: -- 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
  30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  70: -- -- -- -- -- -- -- --
  ```
