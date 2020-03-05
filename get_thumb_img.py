# -*- Coding: utf-8 -*-
import requests
import json
import os
import codecs
import pathlib
import cv2
import sys

def main():
    path_base = os.path.dirname(os.path.abspath(__file__))

    f = codecs.open('output.json', 'r', 'utf-8')
    json_load = json.load(f)

    target_dir = path_base + '/thumb_images2/'
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    target_list = ['http://embed.pixiv.net/decorate.php?illust_id=' + str(p['id']) + '&mode=sns-automator' for p in json_load]
    path_list = [pathlib.Path(target_dir + str(p['id']) + '.png') for p in json_load]

    for target, output in zip(target_list, path_list):
        if len(sys.argv) > 1 and sys.argv[1] == 'resize':
            if os.path.exists(str(output)):
                print(str(output))
                img = cv2.imread(str(output))
                resized_img = cv2.resize(img, (128, 128))
                cv2.imwrite(str(output), resized_img)
        else:
            response = requests.get(target)
            image = response.content

            with open(output, 'wb') as f:
                f.write(image)


    return

if __name__ == '__main__':
    main()
