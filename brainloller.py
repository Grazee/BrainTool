import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


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


def encode(image_name, bfcode, new_name = 'empty', need_save = 1):
    if new_name == 'empty':
        new_name = image_name[:-4] + '_encoded'
    old_img = load_img(image_name)
    new_img = code_to_img(bfcode)
    img = change_img(old_img, new_img)
    if not need_save:
        return img
    save_img(new_name, img)
    return "Encode successful"
    
def decode(img):
    res = ''
    direction = 0
    x = 0
    y = 0
    while True:
        i = img.getpixel((x, y))
        if i not in color_map:
            break
        code = color_map[i]
        if code == 'L':
            direction = (direction - 1) % 4
        elif code == 'R':
            direction = (direction + 1) % 4
        else:
            res += code
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
    img = Image.open('images/a.png')
    # print(img.getpixel((0,0)))
    print(decode(img))
