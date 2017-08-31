from PIL import Image
import os, sys
import copy

def toGrayscale(im_orig):
    im_gray = im_orig.convert("L")
    return im_gray

def toCheckered(im_orig):
    im_check = copy.copy(im_orig)
    width, height = im.size
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            try:
                im_check.putpixel((x, y), (255, 0, 0))
            except IndexError as err:
                print("Error colouring pixel at ({}, {})".format(x, y))
    return im_check

def fizzleFibonacci(im_orig):
    # FIBONACCI IMPLEMENTATION
    # A maximum length Linear Feedback Shift Register of 17 bits
    # 8 to produce a Y value, 9 for an X value
    im_fizzle = copy.copy(im_orig)
    lsfr = [0] * 16 + [1]
    lsfr_start = lsfr
    lsfr = shiftFibonacci(lsfr)
    im.putpixel((0, 0), (255, 0, 0))
    im.putpixel((0, 1), (255, 0, 0))
    while lsfr != lsfr_start:
        lsfr = shiftFibonacci(lsfr)
        x, y = toInt(lsfr[:9]), toInt(lsfr[9:])
        try:
            im_fizzle.putpixel((x, y), (255, 0, 0))
        except:
            pass
    return im_fizzle

def shiftFibonacci(curr_state):
    lsb = (curr_state[13] + curr_state[16]) % 2
    shift_state = [lsb] + curr_state[:16]
    return shift_state

def toInt(bit_array):
    n = 0
    index = 0
    while bit_array:
        n += bit_array.pop() * (2 ** index)
        index += 1
    return n


for infile in sys.argv[1:]:
    file, ext = os.path.splitext(infile)
    gray_file = file + "_gray.jpg"
    checkered_file = file + "_checkered.jpg"
    fizzle_file = file + "_fizzlefade.jpg"
    try:
        im = Image.open(infile)

        im_gray = toGrayscale(im)
        im_gray.save(gray_file)

        im_check = toCheckered(im)
        im_check.save(checkered_file)

        im_fizzle = fizzleFibonacci(im)
        im_fizzle.save(fizzle_file)

    except IOError as err:
        print("Could not convert '{}': '{}'".format(infile, err))



# def shift_lsfr(current_state):
#     # pass tap 14 and 17 through an XOR gate
#     lsb = (current_state[13] + current_state[16]) % 2
#     shift_state = [lsb] + current_state[:16]
#     return shift_state
#
#
# lsfr = [0] * 16 + [1]
# lsfr_start = lsfr
# lsfr = shift_lsfr(lsfr)
# iterations = 1
# while lsfr != lsfr_start:
#     lsfr = shift_lsfr(lsfr)
#     iterations += 1
#
# print(iterations)