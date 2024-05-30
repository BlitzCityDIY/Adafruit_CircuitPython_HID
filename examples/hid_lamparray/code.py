import board
import time
import digitalio
import analogio
import usb_hid
import neopixel

from HID_LampArray import LampArrayKind, MicrosoftHidLampArray, LampArrayColor
print(usb_hid.devices)
# lamp = HID_LampArray(usb_hid.devices)
# lamp = HID_LampArray(usb_hid.devices, 5, board.NEOPIXEL)

NEO_PIXEL_PIN = board.NEOPIXEL
NEO_PIXEL_LAMP_COUNT = 1
NEO_PIXEL_TYPE = neopixel.GRB
NEO_PIXEL_LAMP_UPDATE_LATENCY = 4

# Initialize NeoPixel
neo_pixel_strip = neopixel.NeoPixel(NEO_PIXEL_PIN, NEO_PIXEL_LAMP_COUNT, pixel_order=NEO_PIXEL_TYPE)

# Create lamp array
lamp_array = MicrosoftHidLampArray(usb_hid.devices, NEO_PIXEL_LAMP_COUNT, 70, 55, 1, LampArrayKind.LampArrayKindPeripheral, NEO_PIXEL_LAMP_UPDATE_LATENCY)

# Autonomous mode color
autonomous_color = (0, 0, 255)

# Initialize
neo_pixel_strip.fill(autonomous_color)
neo_pixel_strip.show()

# Main loop
while True:
    current_lamp_array_state = [LampArrayColor(0, 0, 0, 0) for _ in range(NEO_PIXEL_LAMP_COUNT)]
    is_autonomous_mode = lamp_array.get_current_state(current_lamp_array_state)
    update = False
    for i in range(NEO_PIXEL_LAMP_COUNT):
        new_color = autonomous_color if is_autonomous_mode else (
            current_lamp_array_state[i].red_channel,
            current_lamp_array_state[i].green_channel,
            current_lamp_array_state[i].blue_channel
        )
        if new_color != neo_pixel_strip[i]:
            neo_pixel_strip[i] = new_color
            update = True

    if update:
        neo_pixel_strip.show()
