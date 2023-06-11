import math

from PIL import Image
import colorsys


# for reference
def unpack_rrrgggbb(uint8):
    r = (uint8 & 0b11100000) >> 5
    g = (uint8 & 0b00011100) >> 2
    b = (uint8 & 0b00000011)
    return r, g, b


# for reference
def pack_rrrgggbb(rgb: tuple):
    return int(rgb[2]) + (int(rgb[1]) << 2) + (int(rgb[0]) << 5)


def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


def generate_palette_hsv(d: int):
    pixels = []
    for x in range(int(math.pow(d, 2))):
        h = ((x % d) / d) * 360
        s = clip((math.floor((x / d) + 1) / (d / 1.5)) * 99, 0, 100)
        v = clip(abs((math.floor(x / d) - d) / (d / 1.5)) * 99, 0, 100)
        rgb = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h / 360, s / 100, v / 100))
        pixels.append(rgb)
        # print(f"x: {x}, row: {math.floor(x / 16)}, hsv: {h},{s},{v}, rgb: {rgb}")

    return pixels


if __name__ == '__main__':
    d = 16  # dimensions (d*d)
    with Image.new('RGB', (d, d)) as im:
        pixels = generate_palette_hsv(d)
        for p in range(len(pixels)):
            x = (p % d)
            y = int((math.floor(p / d) / (d - 1)) * (d - 1))
            im.putpixel((x, y), pixels[p])
            # print(f"{x},{y}: {pixels[p]}")

        print(len(set(im.getdata())))
        im.show()
        bits = math.exp(math.log(d*d)/10)
        im.save(f"output.png")
