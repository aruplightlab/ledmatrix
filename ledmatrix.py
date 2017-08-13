#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2017-08-14 Francesco Anselmo

HOST = "localhost"
PORT = 4223

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import BrickletLEDStrip
from PIL import Image, ImageDraw, ImageFont
from time import sleep

MATRIX_DIM = (24,8)
TILE_DIM = (3,1)
FONT = 'font/arial.ttf'
FONTSIZE = 8

RESIZE = 10

LED_BRICKLET = 231

TEXT = "TEST"

ipcon = IPConnection()

def draw(led_bricklet, text):
    font_t = ImageFont.truetype(FONT, FONTSIZE)
    image = Image.new('RGB',MATRIX_DIM,(0,0,0))
    d = ImageDraw.Draw(image)
    d.text((0, 0), TEXT, fill=(100,0,0), font=font_t)
    image_resized = image.resize((image.size[0]*RESIZE,image.size[1]*RESIZE))
    # image_resized.show()
    image_data = image.load()
    # print(image_data)
    # print(image_data[0,0])
    # Set first 10 LEDs to green
    # r = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # g = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0]
    # b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # led_bricklet.set_rgb_values(0, 10, r, g, b)

    index = 0
    for tx in range(TILE_DIM[0]):
        for ty in range(TILE_DIM[1]):
            x1 = tx*(image.size[0]/(TILE_DIM[0]))
            y1 = ty*(image.size[1]/(TILE_DIM[1]))
            x2 = tx*(image.size[0]/(TILE_DIM[0])) + image.size[0]/(TILE_DIM[0])
            y2 = ty*(image.size[1]/(TILE_DIM[1])) + image.size[1]/(TILE_DIM[1])
            print(tx, ty, x1, y1, x2, y2)
            area = (x1, y1, x2, y2)
            cropped_img = image.crop(area)
            image_resized = cropped_img.resize((cropped_img.size[0]*RESIZE,cropped_img.size[1]*RESIZE))
            #image_resized.show()
            image_data = cropped_img.load()
            for y in range(cropped_img.size[1]):
                r = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                g = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                for x in range(cropped_img.size[0]):
                    print(image_data[x,y][0], image_data[x,y][1], image_data[x,y][2])
                    r[x] = image_data[x,y][0]
                    g[x] = image_data[x,y][1]
                    b[x] = image_data[x,y][2]

                size = cropped_img.size[0]
                print("index =", index)
                print("size =", size)
                led_bricklet.set_rgb_values(index, size,r,g,b)
                index += cropped_img.size[0]#tx + y*x


    sleep(1)

# Print incoming enumeration
def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    print("UID:               " + uid)
    print("Enumeration Type:  " + str(enumeration_type))

    if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
        print("")
        return

    print("Connected UID:     " + connected_uid)
    print("Position:          " + position)
    print("Hardware Version:  " + str(hardware_version))
    print("Firmware Version:  " + str(firmware_version))
    print("Device Identifier: " + str(device_identifier))
    print("")

    if device_identifier == LED_BRICKLET:
        print(device_identifier, uid, ipcon)
        led_bricklet = BrickletLEDStrip(uid,ipcon)
        draw(led_bricklet, TEXT)

if __name__ == "__main__":
    # Connect to brickd
    ipcon.connect(HOST, PORT)

    # Register Enumerate Callback
    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)

    # Trigger Enumerate
    ipcon.enumerate()

    # for device in ipcon.devices:
    #     print(device)
    #     print(dir(device))

    sleep(1)


    ipcon.disconnect()
