from PIL import Image           # http://pillow.readthedocs.io/en/latest/
import imageio                  # http://imageio.readthedocs.io/en/latest/
import os, sys
import copy, numpy, math


# TODO Investigate methods/libraries to compress/optimise gifs
# TODO Implement Galois Method for LFSR
# TODO Extend fizzle to phase between images


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
        imageio.mimwrite(filepath, fizzle_sequence, subrectangles=True)
    except Exception as error:
        print(error)


def fizzle(im_orig, method="Fibonacci"):

    if method == "Fibonacci":
        # FIBONACCI IMPLEMENTATION
        # Currently uses a maximum length Linear Feedback Shift Register
        # This means the maximum size for an image we can fizzle is 512x512, 1024x256, etc...

        im_fizzle = copy.copy(im_orig)              # create a new instance of the image object
        # Refer here for max-length LFSR taps: http://www.xilinx.com/support/documentation/application_notes/xapp052.pdf
        lfsr_taps = {14: [0, 2, 4, 13],
                     15: [13, 14],
                     16: [3, 12, 14, 15],
                     17: [13, 16],
                     18: [10, 17],
                     19: [0, 1, 5, 18],
                     20: [16, 19]}

        width, height = im_fizzle.size
        width_bitwise = math.ceil(math.log(width, 2))
        height_bitwise = math.ceil(math.log(height, 2))

        fizzle_sequence = [numpy.array(im_fizzle)]
        lfsr = [0] * (width_bitwise + height_bitwise)
        ticker = 2 ** (width_bitwise + height_bitwise - 5)
        lfsr[-1] = 1
        lfsr_start = lfsr
        lfsr = shift_fibonacci(lfsr, lfsr_taps)
        im_fizzle.putpixel((0, 0), (255, 0, 0))    # LSFR can only can be entirely zeroes if it is the start state
        im_fizzle.putpixel((0, 1), (255, 0, 0))    # color the start state

        loop_count = 0
        while lfsr != lfsr_start:
            lfsr = shift_fibonacci(lfsr, lfsr_taps)
            x, y = convert_binary_to_int(lfsr[:width_bitwise]), convert_binary_to_int(lfsr[width_bitwise:])
            try:
                im_fizzle.putpixel((x, y), (255, 0, 0))
                if loop_count % ticker == 0:
                    fizzle_sequence.append(numpy.array(im_fizzle))
            except IndexError:
                pass                                # fading a pixel outside the image dimensions
            except KeyError:
                raise Exception("The shift register is either too large or too small")
            loop_count += 1
            
        # leave the end image for a moment before looping
        for _ in range(10):
            fizzle_sequence.append(numpy.array(im_fizzle))

    # elif method == "Galois":
    #     # GALOIS IMPLEMENTATION
    #     #
    #     fizzle_sequence = []

    else:
        raise Exception("Unknown fizzle method chosen: {}".format(method))

    return fizzle_sequence


def shift_fibonacci(current_register, taps):
    # Calculate the shift bit from reading the taps of the current register, return a new shifted array

    register_length = len(current_register)

    if register_length not in taps:
        raise KeyError

    lsb = 0
    for tap in taps[register_length]:
        lsb += current_register[tap]
    lsb %= 2
    shift_register = [lsb] + current_register[:-1]
    return shift_register


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
