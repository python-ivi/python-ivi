"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import io
import struct
import numpy as np

def parse_hprtl(rtl_file):
    """Convert HP Raster Transfer Language (RTL) to numpy array"""
    color = 1
    width = 0
    byte_width = 0
    height = 0
    compression = 0

    current_row = 0
    plane_cnt = 1
    current_plane = 0

    resolution = 1

    plane_data = None

    in_raster = False

    red = 0
    green = 0
    blue = 0

    color_list = [
        (255, 255, 255), # white
        (  0,   0,   0) # black
    ]

    if type(rtl_file) == str:
        rtlf = open(rtl_file, 'rb')
    else:
        rtlf = rtl_file

    while True:
        s = rtlf.read(1)

        if len(s) == 0:
            break

        if s[0] != 0x1b:
            continue

        s = rtlf.read(1)

        if len(s) == 0:
            break

        if s[0] == ord('*'):
            # valid ESC* command
            # read [letter][numbers][letter]
            cmd = rtlf.read(2)

            while True:
                if (cmd[-1] < ord('0') or cmd[-1] > ord('9')) and cmd[-1] != ord('-'):
                    break

                s = rtlf.read(1)

                # ignore null bytes
                if s[0] != 0:
                    cmd += s

            ca = cmd[0]
            cb = cmd[-1]

            #print(cmd)

            if ca == ord('r') and (cb == ord('u') or cb == ord('U')):
                # color command *r#u or *r#U
                color = int(cmd[1:-1])

                if color == -4:
                    # KCMY
                    plane_cnt = 4
                    color_list = [
                        (255, 255, 255), # white
                        (127, 127, 127), # white
                        (  0, 255, 255), # cyan
                        (  0, 127, 127), # cyan
                        (255,   0, 255), # magenta
                        (127,   0, 127), # magenta
                        (  0,   0, 255), # blue
                        (  0,   0, 127), # blue
                        (255, 255,   0), # yellow
                        (127, 127,   0), # yellow
                        (  0, 255,   0), # green
                        (  0, 127,   0), # green
                        (255,   0,   0), # red
                        (127,   0,   0), # red
                        ( 63,  63,  63), # black
                        (  0,   0,   0) # black
                    ]
                elif color == -3:
                    # CMY
                    plane_cnt = 3
                    color_list = [
                        (255, 255, 255), # white
                        (  0, 255, 255), # cyan
                        (255,   0, 255), # magenta
                        (  0,   0, 255), # blue
                        (255, 255,   0), # yellow
                        (  0, 255,   0), # green
                        (255,   0,   0), # red
                        (  0,   0,   0)  # black
                    ]
                elif color == 1:
                    # K
                    plane_cnt = 1
                    color_list = [
                        (255, 255, 255), # white
                        (  0,   0,   0) # black
                    ]
                elif color == 3:
                    # RGB
                    plane_cnt = 3
                    color_list = [
                        (  0,   0,   0), # black
                        (255,   0,   0), # red
                        (  0, 255,   0), # green
                        (255, 255,   0), # yellow
                        (  0,   0, 255), # blue
                        (255,   0, 255), # magenta
                        (  0, 255, 255), # cyan
                        (255, 255, 255)  # white
                    ]
                elif color == 4:
                    # indexed RGB
                    plane_cnt = 4
                    color_list = [
                        (  0,   0,   0), # black
                        (  0,   0,   0), # black
                        (127,   0,   0), # red
                        (255,   0,   0), # red
                        (  0, 127,   0), # green
                        (  0, 255,   0), # green
                        (127, 127,   0), # yellow
                        (255, 255,   0), # yellow
                        (  0,   0, 127), # blue
                        (  0,   0, 255), # blue
                        (127,   0, 127), # magenta
                        (255,   0, 255), # magenta
                        (  0, 127, 127), # cyan
                        (  0, 255, 255), # cyan
                        (127, 127, 127),  # white
                        (255, 255, 255)  # white
                    ]
                else:
                    raise Exception("Invalid color")
            elif ca == ord('r') and (cb == ord('a') or cb == ord('A')):
                # start raster graphics
                # if we missed the stop of one section, stop on the start of the next
                if in_raster:
                    in_raster = False
                # only grab the first section
                if height == 0:
                    in_raster = True
            elif ca == ord('r') and (cb == ord('c') or cb == ord('C')):
                # end raster graphics
                in_raster = False
            elif ca == ord('r') and (cb == ord('b') or cb == ord('B')):
                # unknown
                pass
            elif ca == ord('r') and (cb == ord('s') or cb == ord('S')):
                # raster width
                width = int(cmd[1:-1])
                byte_width = int((width+7)/8)
            elif ca == ord('r') and (cb == ord('t') or cb == ord('T')):
                # raster height
                #height = int(cmd[1:-1])
                pass
            elif ca == ord('b') and (cb == ord('m') or cb == ord('M')):
                # set compression
                compression = int(cmd[1:-1])
            elif ca == ord('t') and (cb == ord('r') or cb == ord('R')):
                # set resolution
                resolution = int(cmd[1:-1])
            elif ca == ord('v') and (cb == ord('a') or cb == ord('A')):
                # set red component
                red = int(cmd[1:-1])
            elif ca == ord('v') and (cb == ord('b') or cb == ord('B')):
                # set green component
                green = int(cmd[1:-1])
            elif ca == ord('v') and (cb == ord('c') or cb == ord('C')):
                # set blue component
                blue = int(cmd[1:-1])
            elif ca == ord('v') and (cb == ord('i') or cb == ord('I')):
                # assign index
                ind = int(cmd[1:-1])
                color_list[ind] = (red, green, blue)
            elif ca == ord('b') and (cb == ord('v') or cb == ord('V') or cb == ord('w') or cb == ord('W')):
                # image row
                l = int(cmd[1:-1])

                # read row
                d = rtlf.read(l)

                # skip if we are not in a raster section
                if not in_raster:
                    continue

                # set width if not yet set
                # width must be set if compression enabled, otherwise
                # all lines will be the same length
                if width == 0:
                    width = l * 8

                if byte_width == 0:
                    byte_width = l

                # add row if on first plane
                if current_plane == 0:
                    if height == 0:
                        plane_data = np.zeros((10, byte_width, plane_cnt), dtype=np.uint8)

                    height += 1

                    if height >= plane_data.shape[0]:
                        # need to add more rows
                        plane_data = np.append(plane_data, np.zeros((10, byte_width, plane_cnt), dtype=np.uint8), 0)

                if compression == 0 or compression == 1:
                    x = 0
                    for b in d:
                        plane_data[height-1][x][current_plane] = b
                        x += 1
                elif compression == 2:
                    k = 0
                    x = 0
                    while True:
                        if len(d) <= k:
                            break
                        h = d[k]
                        k += 1
                        if h == 128:
                            continue
                        if h < 128:
                            for j in range(h+1):
                                b = d[k]
                                k += 1
                                plane_data[height-1][x][current_plane] = b
                                x += 1
                        if h > 128:
                            b = d[k]
                            k += 1
                            for j in range(257-h):
                                plane_data[height-1][x][current_plane] = b
                                x += 1
                else:
                    raise Exception("Invalid compression")

                # go to next plane, if more than one plane
                if plane_cnt > 0:
                    current_plane += 1
                    if current_plane == plane_cnt or cb == ord('w') or cb == ord('W'):
                        current_plane = 0

    # convert to bits
    plane_data = np.unpackbits(plane_data, axis=1)

    # strip off extra rows
    plane_data = plane_data[0:height, 0:width, :]

    # convert plane data to RGB
    plane_data = np.right_shift(np.packbits(plane_data, axis=2), 8-plane_cnt)
    
    rgb_data = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            rgb_data[y][x] = color_list[plane_data[y][x][0]]

    plane_data = rgb_data

    return plane_data

def generate_bmp(img_data):
    """Generate a BMP format image from a numpy array"""
    bmp = io.BytesIO()

    width = img_data.shape[1]
    height = img_data.shape[0]

    if img_data.shape[2] == 1:
        # monochrome
        bpp = 1
        color_table_entries = 2

    else:
        # rgb
        bpp = 24
        color_table_entries = 0

    row_size = int((bpp*width + 31)/32)*4
    image_size = row_size * height
    header_size = 14+40
    color_table_size = color_table_entries*4
    image_offset = header_size+color_table_size
    file_size = image_offset+image_size

    # bitmap header
    bmp.write(b'BM')
    bmp.write(struct.pack('<L', file_size)) # file size
    bmp.write(struct.pack('<H', 0)) # reserved
    bmp.write(struct.pack('<H', 0)) # reserved
    bmp.write(struct.pack('<L', image_offset)) # offset to bitmap data
    # bitmapinfoheader
    bmp.write(struct.pack('<L', 40)) # size of header
    bmp.write(struct.pack('<l', width)) # image width
    bmp.write(struct.pack('<l', height)) # image height
    bmp.write(struct.pack('<H', 1)) # number of color planes
    bmp.write(struct.pack('<H', bpp)) # bits per pixel
    bmp.write(struct.pack('<L', 0)) # compression method
    bmp.write(struct.pack('<L', image_size)) # image size
    bmp.write(struct.pack('<L', 1)) # horizontal resolution
    bmp.write(struct.pack('<L', 1)) # vertical resolution
    bmp.write(struct.pack('<L', color_table_entries)) # number of colors in palette (0 = 2^n)
    bmp.write(struct.pack('<L', 0)) # number of important colors in palette (0 = all)

    if img_data.shape[2] == 1:
        # monochrome

        # color table
        bmp.write(struct.pack('<BBBx', 255, 255, 255)) # color 0 red, green, blue
        bmp.write(struct.pack('<BBBx', 0, 0, 0)) # color 1 red, green, blue

        # image data
        plane_data = np.packbits(img_data, axis=1)

        for y in range(plane_data.shape[0]-1, -1, -1):
            for x in range(plane_data.shape[1]):
                bmp.write(struct.pack('<B', plane_data[y][x][0]))
            if plane_data.shape[1] % 4 > 0:
                for x in range(4 - (plane_data.shape[1] % 4)):
                    bmp.write(b'\0')

    else:
        # rgb
        
        # color table
        # no color table for RGB

        # image data
        for y in range(img_data.shape[0]-1, -1, -1):
            for x in range(img_data.shape[1]):
                bmp.write(struct.pack('<BBB', img_data[y][x][2], img_data[y][x][1], img_data[y][x][0]))
            if (img_data.shape[1]*3) % 4 > 0:
                for x in range(4 - ((img_data.shape[1]*3) % 4)):
                    bmp.write(b'\0')

    return bmp.getvalue()

