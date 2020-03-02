from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

input_dir = "dimg"
output_dir = "doraimages_new2"

files = glob.glob(input_dir + '/*.jpg')

if os.path.isdir(output_dir) == False:
    os.mkdir(output_dir)


for i, file in enumerate(files):

    img = load_img(file)
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)

    datagen = ImageDataGenerator(
        rotation_range=7,
        width_shift_range=0.1,
        zoom_range=0.1,
        shear_range=0.03,
        channel_shift_range=30,
    )

    g = datagen.flow(x, batch_size=1, save_to_dir=output_dir, save_prefix='', save_format='jpg')
    for index in range(8):
        batch = g.next()
