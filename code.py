import time, gc, os
import neopixel
import board, digitalio
import feathers3

pins_to_toggle = [
    board.D5,
    board.D6,
    board.D9,
    board.D10,
    board.D11,
    board.D14,
    board.D15,
    board.D16,
    board.D17,
    board.D18,
]
pins = []


def InitPins():
  global pins, pins_to_toggle
  for pin_num in pins_to_toggle:
    pin = digitalio.DigitalInOut(pin_num)
    pin.direction = digitalio.Direction.OUTPUT
    pins.append(pin)


def ToggleLEDs():
  feathers3.led_blink()
  for pin in pins:
    pin.value = False if pin.value else True


# Create a NeoPixel instance
# Brightness of 0.3 is ample for the 1515 sized LED
pixel = neopixel.NeoPixel(board.NEOPIXEL,
                          1,
                          brightness=0.3,
                          auto_write=True,
                          pixel_order=neopixel.GRB)

# Say hello
print("\nHello from FeatherS3!")
print("------------------\n")

# Show available memory
print("Memory Info - gc.mem_free()")
print("---------------------------")
print("{} Bytes\n".format(gc.mem_free()))

flash = os.statvfs('/')
flash_size = flash[0] * flash[2]
flash_free = flash[0] * flash[3]
# Show flash size
print("Flash - os.statvfs('/')")
print("---------------------------")
print("Size: {} Bytes\nFree: {} Bytes\n".format(flash_size, flash_free))

print("Pixel Time!\n")

# Create a colour wheel index int
color_index = 0

# Turn on the power to the NeoPixel
feathers3.set_ldo2_power(True)

InitPins()

# Rainbow colors on the NeoPixel
while True:
  # Get the R,G,B values of the next color
  r, g, b = feathers3.rgb_color_wheel(color_index)
  # Set the color on the NeoPixel
  pixel[0] = (r, g, b, 0.5)
  # Increase the wheel index
  color_index += 1

  # If the index == 255, loop it
  if color_index == 255:
    color_index = 0
    # Invert the internal LED state every half color cycle
    ToggleLEDs()

  # Sleep for 15ms so the color cycle isn't too fast
  time.sleep(0.015)
