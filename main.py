import math

from PIL import Image
import colorsys


def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


def generate_palette_hsv():
    pixels = []
    for x in range(256):
        h = ((x % 16) / 16) * 360
        s = clip((math.floor((x / 16) + 2) / 9) * 99, 0, 100)
        v = clip(abs((math.floor(x / 16) - 16) / 9) * 99, 0, 100)
        rgb = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h / 360, s / 100, v / 100))
        pixels.append(rgb)
        print(f"x: {x}, row: {math.floor(x / 16)}, hsv: {h},{s},{v}, rgb: {rgb}")

    return pixels


def unpack_rrrgggbb(uint8):
    r = (uint8 & 0b11100000) >> 5
    g = (uint8 & 0b00011100) >> 2
    b = (uint8 & 0b00000011)
    return r, g, b


def pack_rrrgggbb(rgb: tuple):
    return int(rgb[2]) + (int(rgb[1]) << 2) + (int(rgb[0]) << 5)


if __name__ == '__main__':
    with Image.new('RGB', (16, 16)) as im:
        pixels = generate_palette_hsv()
        for p in range(len(pixels)):
            x = (p % 16)
            y = int((math.floor(p / 16) / 15) * 15)
            im.putpixel((x, y), pixels[p])
            #print(f"{x},{y}: {p}")

        print(len(set(im.getdata())))
        im.show()
