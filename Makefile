PORT=/dev/cu.usbserial-0001
PORT=/dev/cu.usbmodem01
CHIP=esp32s2

# These work on macOS for Feather S2.
# See https://feathers2.io/
# May need to modified for Windows/Linux.

.PHONY: getid
getid:
	esptool.py --port ${PORT} chip_id

.PHONY: erase
erase:
	esptool.py --chip ${CHIP} --port ${PORT} erase_flash

.PHONY: bootloader
bootloader:
	esptool.py --chip ${CHIP} --port ${PORT} --baud 460800 write_flash -z 0x1000 feathers2/tinyuf2/combined.bin

.PHONY: micropython
micropython:
	esptool.py --chip ${CHIP} --port ${PORT} write_flash -z 0x1000 feathers2/MicroPython/featherS2-20210902-v1.17.bin
