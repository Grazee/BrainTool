import sys
import argparse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

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

def draw_img(img, bgr=False):
    plt.figure(figsize=(10, 14))
    plt.axis('off')
    plt.imshow(img)
    plt.show()

def load_img(path):
    img = Image.open(path)
    return img
    # img = cv2.imread(path)
    # b, g, r = cv2.split(img) # по умолчанию cv2 почему-то отдает цвета в порядке BGR вместо RGB
    # new_image = cv2.merge([r, g, b])
    # return new_image

def save_img(name, image, exp = 'png'):
    name = '{}.{}'.format(name, exp)
    if '.' in name:
        name = '{}'.format(name)
    cv2.imwrite(name,image[:,:,::-1])
    print(name + " saved!")

def change_img(old, img):
    x = old.shape[0]
    y = old.shape[1]
    old = old.reshape(x*y, 3)
    img = img.reshape(img.shape[1], 3)
    for i in range(min(img.shape[0], old.shape[0]//10)):
        old[i] = img[i]
    return old.reshape(x,y,3)

def code_to_img(code):
    res = []
    for i in code:
        for j in d.keys():
            if d[j] == i:
                res.append((j))
                break
    img = np.array([res])
    return img


def encod(image_name, bfcode, new_name = 'empty', need_save = 1):
    if new_name == 'empty':
        new_name = image_name[:-4] + '_encoded'
    old_img = load_img(image_name)
    new_img = code_to_img(bfcode)
    img = change_img(old_img, new_img)
    if not need_save:
        return img
    save_img(new_name, img)
    return "Encode successful"

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
                    img.save(open(img_path, 'wb'))
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
                    img.save(open(img_path, 'wb'))                    
                    return

            # turning
            img.putpixel((0, y), code_map['L'])    
    
def decode(img_path, out_path):
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

    with open(out_path, 'w') as f_out:
        f_out.write(res)
        f_out.close()


if __name__ == '__main__':
    usage_text = """
    Brainloller in python to convert brainf**k code to or from image.

example:
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
        encode(args.in_file,
               args.out_file,
               int(args.img_width))
    elif usage == 'decode' and args.in_file and args.out_file:
        decode(args.in_file,
               args.out_file)
    else:
        parser.print_help()
