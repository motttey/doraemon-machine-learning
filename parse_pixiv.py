# -*- Coding: utf-8 -*-
from pixivpy3 import *
import json
import sys
import csv
import codecs

if __name__ == '__main__':
    args = sys.argv
    user_id = args[1]
    password = args[2]
    user_num = int(args[3])

    illust_count = 0
    illust_total_view = 0
    illust_total_bookmark = 0
    illust_total_comments = 0

    manga_count = 0
    manga_total_view = 0
    manga_total_bookmark = 0
    manga_total_comments = 0

    each_illusts = []

    each_years = {
        "2018": [],
        "2017": [],
        "2016": [],
        "2015": [],
        "2014": [],
        "2013": [],
        "2012": [],
        "2011": [],
        "2010": [],
        "2009": [],
        "2008": []
    }

    if len(args) > 3:
        api = AppPixivAPI()
        api.login(user_id, password)

        json_result = api.user_illusts(user_num)
        for illust in json_result.illusts:
            print(illust.create_date.split('-')[0])
            year = illust.create_date.split('-')[0]
            each_years[year].append(illust.id)

            illust_count = illust_count + 1
            illust_total_view = illust_total_view + illust.total_view
            illust_total_bookmark = illust_total_bookmark + illust.total_bookmarks
            illust_total_comments = illust_total_comments + illust.total_comments

            each_illusts.append(
            {
                "id": illust.id,
                "view": illust.total_view,
                "bookmark": illust.total_bookmarks,
                "comments": illust.total_comments,
                "url": illust.image_urls['large'],
                "tags": illust.tags,
                "width": illust.width,
                "height": illust.height,
            })

        next_url = json_result.next_url
        flag = 0

        while flag == 0:
            try:
                next_qs = api.parse_qs(next_url)
                next_result = api.user_illusts(**next_qs)

                for illust in next_result.illusts:
                    year = illust.create_date.split('-')[0]
                    each_years[year].append(illust.id)

                    illust_count = illust_count + 1
                    illust_total_view = illust_total_view + illust.total_view
                    illust_total_bookmark = illust_total_bookmark + illust.total_bookmarks
                    illust_total_comments = illust_total_comments + illust.total_comments

                    each_illusts.append(
                    {
                        "id": illust.id,
                        "view": illust.total_view,
                        "bookmark": illust.total_bookmarks,
                        "comments": illust.total_comments,
                        "url": illust.image_urls['large'],
                        "tags": illust.tags,
                        "width": illust.width,
                        "height": illust.height,
                    })
                next_url = next_result.next_url
                print(next_url)
            except Exception as e:
                print("end")
                flag = 1

        json_result_manga = api.user_illusts(user_num, type="manga")
        for manga in json_result_manga.illusts:
            print(manga.create_date.split('-')[0])
            year = manga.create_date.split('-')[0]

            each_years[year].append(manga.id)
            # for page in manga.meta_pages:
            #    each_years[year].append(page)

            manga_count = manga_count + len(manga.meta_pages)
            manga_total_view = manga_total_view + manga.total_view
            manga_total_bookmark = manga_total_bookmark + manga.total_bookmarks
            manga_total_comments = manga_total_comments + manga.total_comments

            each_illusts.append(
            {
                "id": manga.id,
                "view": manga.total_view,
                "bookmark": manga.total_bookmarks,
                "comments": manga.total_comments,
                "url": manga.image_urls['large'],
                "tags": manga.tags,
                "width": manga.width,
                "height": manga.height,
            })

        next_url = json_result_manga.next_url
        flag = 0

        while flag == 0:
            try:
                next_qs = api.parse_qs(next_url)
                next_result = api.user_illusts(**next_qs)

                for illust in next_result.illusts:
                    year = illust.create_date.split('-')[0]

                    each_years[year].append(manga.id)
                    #for page in manga.meta_pages:
                    # each_years[year].append(page)

                    manga_count = manga_count + len(manga.meta_pages)
                    manga_total_view = manga_total_view + manga.total_view
                    manga_total_bookmark = manga_total_bookmark + manga.total_bookmarks
                    manga_total_comments = manga_total_comments + manga.total_comments

                    each_illusts.append(
                    {
                        "id": manga.id,
                        "view": manga.total_view,
                        "bookmark": manga.total_bookmarks,
                        "comments": manga.total_comments,
                        "url": manga.image_urls['large'],
                        "tags": manga.tags,
                        "width": manga.width,
                        "height": manga.height,
                    })
                next_url = next_result.next_url
                print(next_url)
            except Exception as e:
                print("end")
                flag = 1

    for key, values in each_years.items():
        print(str(key) + ":" + str(len(values)))

    print(illust_count + manga_count)
    print(illust_total_view + manga_total_view)
    print(illust_total_bookmark + manga_total_bookmark)
    print(illust_total_comments + illust_total_comments)

    print(manga_count)
    print(manga_total_view)
    print(manga_total_bookmark)
    print(manga_total_comments)

    f = codecs.open("output.json", "w", "utf-8")
    json.dump(each_illusts, f, ensure_ascii=False)
