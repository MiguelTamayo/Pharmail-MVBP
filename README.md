# Pharmail-MVBP

## Components Used

- Raspberry Pi Zero W

<img src="/img/Raspberry_Pi_Zero_WH.jpg" width="400">

- HX711 Load Cell Amplifier

<img src="/img/HX711.jpg" width="400">

- 10KG Load Cell

<img src="/img/10KG_Load_Cell.jpg" width="400">

- Magnetic Reed Switch

<img src="/img/Magnetic_Reed_Switch.jpg" width="400">

- 5K Resistor


## Libraries

- RPi.GPIO

- twilio

- hx711 (https://github.com/tatobari/hx711py)


## External API Dependencies

SMS notification done via:
- https://www.twilio.com/


## References
https://www.kjmagnetics.com/blog.asp?p=raspberry-pi-alarm
https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/


## Notes

The required Twilio parameters are not available, you will need to use your account's tokens and phone numbers to have function SMS notification

The mailbox_monitoring.py script referenceUnit has a value of 594 because that was what my calculation was after following the steps in the example.py file in (https://github.com/tatobari/hx711py). This value will most likely be different for anyone else and will require to re-calculate the referenceUnit for your setup

The magnetic reed switch has one wire connected to pin 18 using the BCM GPIO configuration, and the other wire connected to a 5K resistor which is then connected to a ground pin on the PI. I am unsure as to whether the resistor is even needed but I added it as a safety precaution and everything appears to work fine with it.

For the HX711 and Load Cell wiring follow the tutorial at (https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/)
