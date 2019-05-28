from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

input_dir = "dd/doraimages2"
output_dir = "dd/doraimages_new/imgs3"

files = glob.glob(input_dir + '/*.jpg')

if os.path.isdir(output_dir) == False:
    os.mkdir(output_dir)


for i, file in enumerate(files):

    img = load_img(file)
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)

    datagen = ImageDataGenerator(
        rotation_range=45,
        horizontal_flip=True,
        width_shift_range=0.05,
        zoom_range=[0.8, 1.1],
        shear_range=0.1,
        channel_shift_range=50,
        brightness_range=[0.7, 1.0],
    )

    g = datagen.flow(x, batch_size=1, save_to_dir=output_dir, save_prefix='', save_format='jpg')
    for index in range(24):
        batch = g.next()
