import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt

if os.path.isdir("./ex01"):
    os.chdir("./ex01")
    from ex01 import util

img = Image.open("img/cat_02.jpg")
img_array = np.asarray(img)
print(img_array.shape)


def radius(img_arr):
    # calculate radius (distance r to centre of image)
    # r of point x, y to centre of image
    # to easy, we move a coordinate to centre of image, by w - w_c, and h - h_c
    # then w_c, and h_c as (0, 0) of cartesian coordinate (x, y)
    height, width, depth = img_array.shape
    w_c = width / 2
    h_c = height / 2

    # create coordinate vectors (x, y)
    _w = np.arange(width)
    _h = np.arange(height)

    # create a grid points based on coordinates
    # Here we centre or move coordinate centre to point w_c and h_c
    grid = np.meshgrid(_w - w_c, _h - h_c)
    xv, yv = grid
    print(xv.shape, yv.shape)

    # Calculate radius of each point x, y to the centre
    # if we do not move coordinate it will be (x - x_c)² + (y - y_c)²
    # Question: why / (w_c² + h_c²)
    r = np.sqrt(xv ** 2 + yv ** 2) / np.sqrt(w_c ** 2 + h_c ** 2)
    return r


img_vignetted = util.vignetting(np.asarray(img))
plt.subplot(1, 2, 1)
plt.imshow(img)

plt.subplot(1, 2, 2)
plt.imshow(np.uint8(img_vignetted))

plt.show()

# 1-2a-1 setup a design matrix and

# 1-2a-2 desired predictions

# 1-2a-3 data flow graph with loss function

# 1-2a-4 data flow graph with minimizer
