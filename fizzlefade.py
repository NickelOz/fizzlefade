from PIL import Image           # http://pillow.readthedocs.io/en/latest/
import imageio                  # http://imageio.readthedocs.io/en/latest/
import os, sys
import copy, numpy, math


# TODO Handle GIFS with reduced palette
# TODO Implement flexibility for larger/smaller GIFS (outside of 512x512 dimensions)
# TODO Invent more elegant method for determine which frames to include in the GIF


def to_grayscale(im_orig):
    im_gray = im_orig.convert("L")
    return im_gray


def to_checkered(im_orig):
    im_check = copy.copy(im_orig)
    width, height = im.size
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            try:
                im_check.putpixel((x, y), (255, 0, 0))
            except IndexError:
                print("Error colouring pixel at ({}, {})".format(x, y))
    return im_check


def generate_fizzle_gif(im_orig, filepath):
    try:
        print("Parsing your image, doing the magic!")
        fizzle_sequence = fizzle(im_orig, "Fibonacci")
        print("Generating your gif, this could take some time")
        imageio.mimwrite(filepath, fizzle_sequence)
    except Exception as error:
        print(error)


def fizzle(im_orig, method="Fibonacci"):

    if method == "Fibonacci":
        # FIBONACCI IMPLEMENTATION
        # A maximum length Linear Feedback Shift Register of 14 bits
        # This means the maximum size for an image we can fizzle is 512x512, 1024x256, etc...

        im_fizzle = copy.copy(im_orig)              # create a new instance of the image object
        fizzle_sequence = [numpy.array(im_fizzle)]
        lsfr = [0] * 13 + [1]
        lsfr_start = lsfr
        lsfr = shift_fibonacci(lsfr)
        im_fizzle.putpixel((0, 0), (255, 0, 0))    # lsfr can only can be entirely zeroes if it is the start state
        im_fizzle.putpixel((0, 1), (255, 0, 0))    # color the start state

        loop_count = 0
        while lsfr != lsfr_start:
            lsfr = shift_fibonacci(lsfr)
            x, y = convert_binary_to_int(lsfr[:7]), convert_binary_to_int(lsfr[7:])
            try:
                im_fizzle.putpixel((x, y), (255, 0, 0))
                if loop_count % 512 == 0:
                    fizzle_sequence.append(numpy.array(im_fizzle))
            except IndexError:
                pass                                # fading a pixel outside the image dimensions
            loop_count += 1
            
        # leave the end image for a moment before looping
        for _ in range(10):
            fizzle_sequence.append(numpy.array(im_fizzle))
    elif method == "Galois":
        fizzle_sequence = []
    else:
        raise Exception("Unknown fizzle method chosen: {}".format(method))
    return fizzle_sequence


def shift_fibonacci(curr_state):
    # Shift the register right and determine the shift bit using taps on bit 11 and 18
    # Assumes 14 bit register.
    # Refer here for taps: http://www.xilinx.com/support/documentation/application_notes/xapp052.pdf

    if len(curr_state) != 14:
        raise Exception("The given register is not 14 bits long")
    # lsb = (curr_state[10] + curr_state[17]) % 2
    lsb = (((((curr_state[0] + curr_state[2]) % 2) + curr_state[4]) % 2) + curr_state[13]) % 2
    shift_state = [lsb] + curr_state[:13]
    return shift_state


def convert_binary_to_int(bit_array):
    n = 0
    index = 0
    while bit_array:
        n += bit_array.pop() * (2 ** index)
        index += 1
    return n


for infile in sys.argv[1:]:
    file, ext = os.path.splitext(infile)
    # gray_file = file + "_gray.jpg"
    # checkered_file = file + "_checkered.jpg"
    fizzle_file = file + "_fizzle.gif"
    try:
        im = Image.open(infile)

        # im_gray = to_grayscale(im)
        # im_gray.save(gray_file)
        #
        # im_check = to_checkered(im)
        # im_check.save(checkered_file)

        generate_fizzle_gif(im, fizzle_file)

    except IOError as err:
        print("Could not convert '{}': '{}'".format(infile, err))
