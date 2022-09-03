
# Values For the Feather S2 (on macOS).
PORT=/dev/cu.usbmodem01

# These work on macOS for Feather S2.
# See https://feathers2.io/
# May need to modified for Windows/Linux.

.PHONY: getid
getid:
	esptool.py --port ${PORT} chip_id

.PHONY: erases2
erases2:
	esptool.py --chip esp32s2 --port ${PORT} erase_flash

.PHONY: erases3
erases3:
	esptool.py --chip esp32s3 --port ${PORT} erase_flash

.PHONY: bootloaders2
bootloaders2:
	esptool.py --chip esp32s2 --port ${PORT} --baud 460800 write_flash -z 0x1000 feathers2/CircuitPython/tinyuf2/combined.bin

.PHONY: bootloaders3
bootloaders3:
	esptool.py --chip esp32s3 --port ${PORT} --baud 460800 write_flash -z 0x1000 feathers2/CircuitPython/tinyuf2/combined.bin

.PHONY: circuitpythons3
circuitpythons3:
	esptool.py --chip esp32s3 --port ${PORT} write_flash -z 0x1000 adafruit-circuitpython-unexpectedmaker_feathers3-en_US-7.3.3.bin

.PHONY: micropythons2
micropythons2:
	esptool.py --chip esp32s2 --port ${PORT} write_flash -z 0x1000 feathers2/MicroPython/featherS2-20210902-v1.17.bin

.PHONY: micropythons3
micropythons3:
	esptool.py --chip esp32s3 --port ${PORT} write_flash -z 0x1000 feathers2/MicroPython/featherS2-20210902-v1.17.bin
