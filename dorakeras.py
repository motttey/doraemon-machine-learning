# -*- coding: utf-8 -*-
import os
import glob
import math
import random
import pathlib

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.python import keras
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.models import Model, Sequential
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img
from tensorflow.python.keras.layers import LeakyReLU,Dropout,ZeroPadding2D
from tensorflow.python.keras.layers import Activation, BatchNormalization, Reshape, Flatten, Add, Input, Conv2D, Conv2DTranspose, Dense, Input, MaxPooling2D, UpSampling2D, Lambda

def generator_model(img_shape):
    model = Sequential()
    model.add(Dense(128 * 32 * 32, activation="relu", input_shape=(128,)))
    model.add(Reshape((32, 32, 128)))
    model.add(BatchNormalization(momentum=0.8))
    model.add(UpSampling2D())
    model.add(Conv2D(128, kernel_size=3, padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(UpSampling2D())
    model.add(Conv2D(64, kernel_size=3, padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Conv2D(3, kernel_size=3, padding="same"))
    model.add(Activation("tanh"))

    noise = Input(shape=(128,))
    img = model(noise)
    return Model(noise, img)

def discriminator_model(img_shape):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=img_shape, padding="same"))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
    model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    model.summary()

    img = Input(shape=img_shape)
    validity = model(img)
    return Model(img, validity)

def save_imgs(path, imgs, rows, cols):
    base_width = imgs.shape[1]
    base_height = imgs.shape[2]
    channels = imgs.shape[3]
    output_shape = (
        base_height*rows,
        base_width*cols,
        channels
    )
    buffer = np.zeros(output_shape)
    for row in range(rows):
        for col in range(cols):
            img = imgs[row*cols + col]
            buffer[
                row*base_height:(row + 1)*base_height,
                col*base_width:(col + 1)*base_width
            ] = img
    array_to_img(buffer).save(path)

def main():
    data_dir = str(pathlib.Path.cwd()) + "/"
    batch_size = 16
    img_shape = (128,128,3)
    print(data_dir)

    gen = ImageDataGenerator(rescale=1/127.5, samplewise_center=True)
    iters = gen.flow_from_directory(
        directory=data_dir,
        # classes=['doraemon'],
        class_mode=None,
        color_mode='rgb',
        target_size=img_shape[:2],
        batch_size=batch_size,
        shuffle=True
    )

    x_train_batch=next(iters)
    for i in range(3):
        plt.imshow(array_to_img(x_train_batch[i]))

    optimizer = Adam(lr=0.00001, beta_1=0.5)

    generator = generator_model(img_shape)
    discriminator = discriminator_model(img_shape)
    discriminator.trainable = True
    generator.compile(loss='binary_crossentropy', optimizer=optimizer)
    discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    z = Input(shape=(128,))
    img = generator(z)

    discriminator.trainable = False
    valid = discriminator(img)

    generator_containing_discriminator = Model(z, valid)
    generator_containing_discriminator.compile(loss='binary_crossentropy', optimizer=optimizer)

    #saveディレクトリ
    model_save_dir = 'models'
    img_save_dir = 'output_imgs'

    #5×5生成画像生成
    imgs_shape = (4, 4)
    n_img_samples = np.prod(imgs_shape)

    sample_seeds = np.random.uniform(-1, 1, (n_img_samples, 128))

    hist = []
    logs = []

    #保存先フォルダ生成
    os.makedirs(model_save_dir, exist_ok=True)
    os.makedirs(img_save_dir, exist_ok=True)

    Totalstep=500000
    for step, batch in enumerate(iters):
        if len(batch) < batch_size:
            continue
        if step > Totalstep:
            break
        half_batch = int(batch_size / 2)
        z_d = np.random.uniform(-1, 1, (half_batch, 128))

        g_pred = generator.predict(z_d)
        discriminator.trainable = True
        real_loss=discriminator.train_on_batch(batch[:half_batch], np.ones((half_batch, 1)))
        fake_loss=discriminator.train_on_batch(g_pred, np.zeros((half_batch, 1)))
        d_loss = 0.5 * np.add(real_loss, fake_loss)

        z_g = np.random.uniform(-1, 1, (batch_size, 128))
        discriminator.trainable = False
        g_loss = generator_containing_discriminator.train_on_batch(z_g, np.ones((batch_size, 1)))

        logs.append({'step': step, 'd_loss': d_loss[0], 'acc[%]': 100*d_loss[1] , 'g_loss': g_loss})
        print(logs[-1])
        if step%200==0:
            img_path = '{}/generate_{}.png'.format(img_save_dir, step)
            save_imgs(img_path, generator.predict(sample_seeds), rows=imgs_shape[0], cols=imgs_shape[1])
        if step%5000==0:
            generator.save('{}/generator_{}.hd5'.format(model_save_dir, step))
            discriminator.save('{}/discriminator_{}.hd5'.format(model_save_dir, step))
    '''
    Totalstep=30
    generator.load_weights('D:/python/jupyter_notebook/dcgan/models/generator_25000.hd5')
    for step, batch in enumerate(iters):
        if len(batch) < batch_size:
            continue
        if step > Totalstep:
            break
        z_d = np.random.uniform(-1, 1, (batch_size, 100))
        g_pred = generator.predict(z_d)
        img_path = '{}/pred_generate_{}.png'.format(img_save_dir, step)
        save_imgs(img_path, generator.predict(z_d), rows=imgs_shape[0], cols=imgs_shape[1])
    '''
    return

if __name__ == '__main__':
    main()
