# -*- Coding: utf-8 -*-
from pixivpy3 import *
import json
import sys
import csv
import codecs
import os
from time import sleep

def main(user_id, password, user_num):
    illust_count = 0
    illust_total_view = 0
    illust_total_bookmark = 0
    illust_total_comments = 0

    each_illusts = []
    target_dir = './pixiv_images/'
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    if len(args) > 3:
        api = AppPixivAPI()

        api.login(user_id, password)

        json_result = api.user_illusts(user_num)
        for illust in json_result.illusts:
            print(illust.create_date.split('-')[0])
            year = illust.create_date.split('-')[0]

            illust_count = illust_count + 1
            illust_total_view = illust_total_view + illust.total_view
            illust_total_bookmark = illust_total_bookmark + illust.total_bookmarks
            illust_total_comments = illust_total_comments + illust.total_comments

            image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.medium)

            api.download(image_url, path=target_dir, name=str(illust.id) + '.png')

            each_illusts.append(
            {
                "id": illust.id,
                "title": illust.title,
                "date": illust.create_date,
                "caption": illust.caption,
                "view": illust.total_view,
                "bookmark": illust.total_bookmarks,
                "comments": illust.total_comments,
                "url": image_url,
                "tags": illust.tags,
                "width": illust.width,
                "height": illust.height,
            })
            sleep(1)

        next_url = json_result.next_url
        flag = 0

        while flag == 0:
            try:
                next_qs = api.parse_qs(next_url)
                next_result = api.user_illusts(**next_qs)

                for illust in next_result.illusts:
                    year = illust.create_date.split('-')[0]

                    image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.medium)
                    print(image_url)

                    api.download(image_url, path=target_dir, name=str(illust.id) + '.png')

                    illust_count = illust_count + 1
                    illust_total_view = illust_total_view + illust.total_view
                    illust_total_bookmark = illust_total_bookmark + illust.total_bookmarks
                    illust_total_comments = illust_total_comments + illust.total_comments

                    each_illusts.append(
                    {
                        "id": illust.id,
                        "title": illust.title,
                        "date": illust.create_date,
                        "caption": illust.caption,
                        "view": illust.total_view,
                        "bookmark": illust.total_bookmarks,
                        "comments": illust.total_comments,
                        "url": image_url,
                        "tags": illust.tags,
                        "width": illust.width,
                        "height": illust.height,
                    })

                    sleep(1)
                next_url = next_result.next_url
                print(next_url)
            except Exception as e:
                print("end")
                flag = 1

        flag = 0
        while flag == 0:
            try:
                next_qs = api.parse_qs(next_url)
                next_result = api.user_illusts(**next_qs)

                next_url = next_result.next_url
                print(next_url)
            except Exception as e:
                print("end")
                flag = 1

    f = codecs.open("output.json", "w", "utf-8")
    json.dump(each_illusts, f, ensure_ascii=False)

if __name__ == '__main__':
    args = sys.argv
    user_id = args[1]
    password = args[2]
    user_num = int(args[3])

    main(user_id, password, user_num)
