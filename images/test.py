#!/usr/bin/env python

#from PIL import Image
import Image

if __name__ == "__main__":
    result = Image.new("RGB", (1920, 1920))
    img1 = Image.open("map_0.jpg")
    
    result.paste(img1, (0, 0, 640, 640))
    result.paste(img1, (640, 0, 1280, 640))
    result.paste(img1, (1280, 0, 1920, 640))

    result.paste(img1, (0, 640, 640, 1280))
    result.paste(img1, (640, 640, 1280, 1280))
    result.paste(img1, (1280, 640, 1920, 1280))

    result.paste(img1, (0, 1280, 640, 1920))
    result.paste(img1, (640, 1280, 1280, 1920))
    result.paste(img1, (1280, 1280, 1920, 1920))
    
    result.save("./new_img.jpg")
