import time, gc, os
import neopixel
import board, digitalio
import feathers3
import adafruit_logging as logging

pins_ids_to_toggle = [
    board.IO11, # Bank 1 Red
    board.IO10, # Bank 1 Yellow
    board.IO7,  # Bank 1 Green
    board.IO3,  # Bank 1 Blue
    board.D1,   # Bank 2 Red
    board.IO38, # Bank 2 Orange
    board.IO33, # Bank 2 Blue
    board.IO9,  # Bank 3
    board.IO8,  # Bank 3
    board.IO35, # Bank 3 Green
]
pins = []
cycle_neopixel = True
logger = None


def InitPins():
  """Initialize the light control pins."""
  global pins, pins_ids_to_toggle
  for pin_num in pins_ids_to_toggle:
    pin = digitalio.DigitalInOut(pin_num)
    pin.direction = digitalio.Direction.OUTPUT
    pins.append(pin)


def InitNeoPixel():
  """Initialize the NeoPixel."""
  global pixel

  # Brightness of 0.3 is ample for the 1515 sized LED
  pixel = neopixel.NeoPixel(board.NEOPIXEL,
                            1,
                            brightness=0.3,
                            auto_write=True,
                            pixel_order=neopixel.GRB)

  # Turn on the power to the NeoPixel
  feathers3.set_ldo2_power(True)


def PrintBoardInfo():
  """Print the Board info to the console."""

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


def Initialize():
  """Initialize the application."""
  global cycle_neopixel, logger

  logger = logging.getLogger('test')
  logger.setLevel(logging.INFO)

  PrintBoardInfo()
  InitPins()
  if cycle_neopixel:
    InitNeoPixel()


def ToggleLEDs():
  """Toggle all light LED's"""
  global pins, logger

  logger.info('Toggling LEDs')

  feathers3.led_blink()
  for pin in pins:
    pin.value = False if pin.value else True


Initialize()

# Rainbow colors on the NeoPixel 0..255.
color_index = 0
while True:
  if cycle_neopixel:
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
