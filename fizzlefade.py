from PIL import Image
import os, sys

def toGrayscale(im):
    im = im.convert("L")
    return im

def toCheckered(im):
    width, height = im.size
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            try:
                im.putpixel((x, y), (255, 0, 0))
            except IndexError as err:
                print("Error colouring pixel at ({}, {})".format(x, y))
    return im

for infile in sys.argv[1:]:
    file, ext = os.path.splitext(infile)
    gray_file = file + "_gray.jpg"
    checkered_file = file + "_checkered.jpg"
    try:
        im = Image.open(infile)

        im_gray = toGrayscale(im)
        im_gray.save(gray_file)

        im_check = toCheckered(im)
        im_check.save(checkered_file)

    except IOError as err:
        print("Could not convert '{}': '{}'".format(infile, err))