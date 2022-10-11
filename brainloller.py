import sys
import argparse
import brainfuck
from PIL import Image

color_map = {
    (255, 0, 0): ">",  # red
    (128, 0, 0): "<",  # darkred
    (0, 255, 0): "+",  # green
    (0, 128, 0): "-",  # darkgreen
    (0, 0, 255): ".",  # blue
    (0, 0, 128): ",",  # darkblue
    (255, 255, 0): "[",  # yellow
    (128, 128, 0): "]",  # darkyellow
    (0, 255, 255): "R",  # cyan
    (0, 128, 128): "L"  # darkcyan
}

code_map = {
    ">": (255, 0, 0),
    "<": (128, 0, 0),
    "+": (0, 255, 0),
    "-": (0, 128, 0),
    ".": (0, 0, 255),
    ",": (0, 0, 128),
    "[": (255, 255, 0),
    "]": (128, 128, 0),
    "R": (0, 255, 255),
    "L": (0, 128, 128)
}

def encode(bf_path, img_path, width):
    f_bf = open(bf_path, 'r')
    bf = f_bf.read().strip()
    length = len(bf)
    height = 0
    if (length - 2) % (width - 2) == 0:
        height = (length - 2) / (width - 2)
    else:
        height = (length - 2) // (width - 2) + 1

    img = Image.new(mode='RGB', size=(width, height), color='#000000')
    code_index = 1
    for y in range(height):
        if y % 2 == 0:
            # even row
            # turning
            if y == 0:
                # first pixel
                img.putpixel((0, y), code_map[bf[0]])
            else:
                img.putpixel((0, y), code_map['L'])

            # put bf data
            for x in range(1, width - 1):
                img.putpixel((x, y), code_map[bf[code_index]])
                code_index += 1
                if code_index >= length:

                    return

            # turning
            img.putpixel((width - 1, y), code_map['R'])

        else:
            # odd row
            # turning
            img.putpixel((width - 1, y), code_map['R'])

            # put bf data
            for x in range(width - 2, 0, -1):
                img.putpixel((x, y), code_map[bf[code_index]])
                code_index += 1
                if code_index >= length:
                    return img

            # turning
            img.putpixel((0, y), code_map['L'])    
    
def decode(img_path):
    img = Image.open(img_path)
    
    res = ''
    direction = 0
    x = 0
    y = 0
    while True:
        i = img.getpixel((x, y))
        if i not in color_map:
            break
        code = color_map[i]

        # if change direction
        if code == 'L':
            direction = (direction - 1) % 4
        elif code == 'R':
            direction = (direction + 1) % 4
        else:
            res += code

        # go to next pixel
        if direction == 0:
            x += 1
        elif direction == 1:
            y += 1
        elif direction == 2:
            x -= 1
        elif direction == 3:
            y -= 1

    return res


if __name__ == '__main__':
    usage_text = """
    Brainloller in python to convert brainf**k code to or from image.

example:
    python3 brainloller.py run -i [image_file]    
    python3 brainloller.py encode -i [bf_code_file] -o [out_image] -w [target_image_width]
    python3 brainloller.py decode -i [image_file] -o [bf_code_file]
    """
    
    parser = argparse.ArgumentParser(usage_text)
    parser.add_argument('-i', help='file input', type=str, dest='in_file')
    parser.add_argument('-o', help='file output', type=str, dest='out_file')
    parser.add_argument('-w', help='image pixel width', type=str, dest='img_width')

    if len(sys.argv) <= 1:
        parser.print_help()
        exit()

    usage = sys.argv.pop(1)
    
    args = parser.parse_args()

    if usage == 'encode' and args.in_file and args.out_file and args.img_width:
        # encdeo bf to image
        img = encode(args.in_file,
                     int(args.img_width))
        
        # save image to file
        img.save(open(args.out_file, 'wb'))
    elif usage == 'decode' and args.in_file and args.out_file:
        # decode bf from image
        res = decode(args.in_file)
        
        # save result to file
        with open(args.out_file, 'w') as f_out:
            f_out.write(res)
            f_out.close()        
    elif usage == 'run' and args.in_file:
        # decode bf from image
        bf = decode(args.in_file)

        # compile bf code
        res = brainfuck.evaluate(bf)
        print(res)
    else:
        parser.print_help()
